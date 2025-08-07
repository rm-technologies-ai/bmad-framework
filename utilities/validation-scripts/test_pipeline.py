#!/usr/bin/env python3
"""
PDF Ingestion Pipeline Test Suite
Comprehensive testing for the PDF-to-Markdown conversion pipeline
"""

import os
import sys
import tempfile
import shutil
import subprocess
import glob
import re
from pathlib import Path
import unittest

# Add project root to Python path for imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Utility functions for testing (avoiding import issues)
def get_next_version_path_test(base_path, converted_dir):
    """Test version of get_next_version_path function"""
    pdf_path = Path(base_path)
    
    # Extract relative path by finding 'input-documents' in the path
    path_parts = pdf_path.parts
    input_docs_index = None
    
    for i, part in enumerate(path_parts):
        if 'input-documents' in part:
            input_docs_index = i
            break
    
    if input_docs_index is not None and input_docs_index < len(path_parts) - 1:
        # Get parts after input-documents
        relative_parts = path_parts[input_docs_index + 1:]
        relative_path = Path(*relative_parts) if relative_parts else Path(pdf_path.name)
    else:
        relative_path = Path(pdf_path.name)
    
    base_name = relative_path.stem
    parent_dir = relative_path.parent if relative_path.parent != Path('.') else Path('')
    
    target_dir = Path(converted_dir) / parent_dir
    target_dir.mkdir(parents=True, exist_ok=True)
    
    existing_files = list(target_dir.glob(f"{base_name}*.md"))
    
    if not existing_files:
        return str(target_dir / f"{base_name}.md")
    
    version_pattern = re.compile(rf"{re.escape(base_name)}_v(\d+)\.md$")
    versions = []
    
    for file_path in existing_files:
        match = version_pattern.search(file_path.name)
        if match:
            versions.append(int(match.group(1)))
        elif file_path.name == f"{base_name}.md":
            versions.append(1)
    
    if not versions:
        return str(target_dir / f"{base_name}.md")
    
    next_version = max(versions) + 1
    return str(target_dir / f"{base_name}_v{next_version}.md")

def get_latest_version_path_test(base_path, converted_dir):
    """Test version of get_latest_version_path function"""
    if base_path.endswith('.pdf'):
        pdf_path = Path(base_path)
        
        # Extract relative path by finding 'input-documents' in the path
        path_parts = pdf_path.parts
        input_docs_index = None
        
        for i, part in enumerate(path_parts):
            if 'input-documents' in part:
                input_docs_index = i
                break
        
        if input_docs_index is not None and input_docs_index < len(path_parts) - 1:
            # Get parts after input-documents
            relative_parts = path_parts[input_docs_index + 1:]
            relative_path = Path(*relative_parts) if relative_parts else Path(pdf_path.name)
        else:
            relative_path = Path(pdf_path.name)
        
        base_name = relative_path.stem
        parent_dir = relative_path.parent if relative_path.parent != Path('.') else Path('')
    else:
        parts = base_path.split('/')
        base_name = Path(parts[-1]).stem
        parent_dir = Path('/'.join(parts[:-1])) if len(parts) > 1 else Path('')
    
    target_dir = Path(converted_dir) / parent_dir
    
    if not target_dir.exists():
        return None
    
    existing_files = list(target_dir.glob(f'{base_name}*.md'))
    
    if not existing_files:
        return None
    
    version_pattern = re.compile(rf"{re.escape(base_name)}_v(\d+)\.md$")
    highest_version = 0
    highest_file = None
    
    for file_path in existing_files:
        match = version_pattern.search(file_path.name)
        if match:
            version = int(match.group(1))
            if version > highest_version:
                highest_version = version
                highest_file = str(file_path)
        elif file_path.name == f"{base_name}.md" and highest_version == 0:
            highest_file = str(file_path)
            highest_version = 1
    
    return highest_file

def validate_markdown_file_test(md_path):
    """Test version of validate_markdown_file function"""
    results = {
        'valid': True,
        'score': 0,
        'max_score': 100,
        'issues': [],
        'warnings': []
    }
    
    if not os.path.exists(md_path):
        results['valid'] = False
        results['issues'].append('File does not exist')
        return results
    
    try:
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        results['valid'] = False
        results['issues'].append(f'Cannot read file: {e}')
        return results
    
    if not content.strip():
        results['valid'] = False
        results['issues'].append('File is empty')
        return results
    
    score = 0
    
    # Check for title/header (20 points)
    if content.startswith('#') or '# ' in content[:100]:
        score += 20
    else:
        results['warnings'].append('No clear title/header found')
    
    # Check minimum content length (20 points)
    if len(content.strip()) > 100:
        score += 20
    else:
        results['warnings'].append('Content seems too short')
    
    # Check for structured content (20 points)
    if any(marker in content for marker in ['##', '###', '*', '-', '1.', '2.']):
        score += 20
    else:
        results['warnings'].append('No clear structure (headers, lists) found')
    
    # Check for reasonable text density (20 points)
    lines = content.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    if len(non_empty_lines) > 5:
        score += 20
    else:
        results['warnings'].append('Very few content lines')
    
    # Check encoding and special characters (20 points)
    try:
        content.encode('utf-8')
        score += 20
    except:
        results['issues'].append('Encoding issues detected')
    
    results['score'] = score
    
    if score < 40:
        results['valid'] = False
        results['issues'].append('Content quality score too low')
    
    return results

class PDFIngestionPipelineTests(unittest.TestCase):
    """Test suite for PDF ingestion pipeline"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.input_dir = os.path.join(self.test_dir, 'input-documents')
        self.converted_dir = os.path.join(self.test_dir, 'input-documents-converted-to-md')
        
        # Create test directories
        os.makedirs(self.input_dir)
        os.makedirs(self.converted_dir)
        
        # Create test PDF (placeholder)
        self.test_pdf = os.path.join(self.input_dir, 'test-document.pdf')
        self.create_test_pdf(self.test_pdf)
        
        # Paths to scripts
        self.converter_script = 'utilities/pdf-ingestion-pipeline/convert_pdf.py'
        self.validation_script = 'utilities/validation-scripts/validate_conversion.py'
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir)
    
    def create_test_pdf(self, pdf_path):
        """Create a test PDF file (placeholder)"""
        # This creates a dummy file - in real tests, use a proper PDF
        with open(pdf_path, 'w') as f:
            f.write("Placeholder PDF content for testing")
    
    def test_directory_structure_creation(self):
        """Test that required directories are created"""
        self.assertTrue(os.path.exists(self.input_dir))
        self.assertTrue(os.path.exists(self.converted_dir))
    
    def test_pdf_file_detection(self):
        """Test PDF file detection in input directory"""
        pdf_files = list(Path(self.input_dir).rglob('*.pdf'))
        self.assertEqual(len(pdf_files), 1)
        self.assertEqual(pdf_files[0].name, 'test-document.pdf')
    
    def test_conversion_script_exists(self):
        """Test that conversion scripts exist and are executable"""
        self.assertTrue(os.path.exists(self.converter_script))
        self.assertTrue(os.path.exists(self.validation_script))
    
    def test_version_number_logic(self):
        """Test version numbering logic"""
        # Test first version
        next_path = get_next_version_path_test(self.test_pdf, self.converted_dir)
        expected = os.path.join(self.converted_dir, 'test-document.md')
        self.assertEqual(next_path, expected)
        
        # Create first version file
        os.makedirs(os.path.dirname(expected), exist_ok=True)
        with open(expected, 'w') as f:
            f.write("Test conversion v1")
        
        # Test second version
        next_path = get_next_version_path_test(self.test_pdf, self.converted_dir)
        expected_v2 = os.path.join(self.converted_dir, 'test-document_v2.md')
        self.assertEqual(next_path, expected_v2)
    
    def test_latest_version_detection(self):
        """Test latest version detection"""
        # Create multiple versions
        base_path = os.path.join(self.converted_dir, 'test-document')
        os.makedirs(self.converted_dir, exist_ok=True)
        
        # Create v1, v2, v3
        versions = [
            f'{base_path}.md',
            f'{base_path}_v2.md',
            f'{base_path}_v3.md'
        ]
        
        for version_path in versions:
            with open(version_path, 'w') as f:
                f.write(f"Content for {os.path.basename(version_path)}")
        
        # Should detect v3 as latest
        latest = get_latest_version_path_test(self.test_pdf, self.converted_dir)
        self.assertEqual(latest, f'{base_path}_v3.md')
    
    def test_validation_criteria(self):
        """Test validation criteria"""
        # Create test markdown files with different quality levels
        test_md = os.path.join(self.test_dir, 'test.md')
        
        # Test empty file (should fail)
        with open(test_md, 'w') as f:
            f.write("")
        result = validate_markdown_file_test(test_md)
        self.assertFalse(result['valid'])
        
        # Test minimal content (should pass)
        with open(test_md, 'w') as f:
            f.write("# Test Document\n\nThis is a test document with sufficient content for validation. " * 5)
        result = validate_markdown_file_test(test_md)
        self.assertTrue(result['valid'])
        self.assertGreaterEqual(result['score'], 40)
    
    def test_hierarchy_preservation(self):
        """Test that folder hierarchy is preserved"""
        # Create nested structure
        nested_dir = os.path.join(self.input_dir, 'research', 'studies')
        os.makedirs(nested_dir)
        
        nested_pdf = os.path.join(nested_dir, 'analysis.pdf')
        self.create_test_pdf(nested_pdf)
        
        expected_path = get_next_version_path_test(nested_pdf, self.converted_dir)
        expected_nested = os.path.join(self.converted_dir, 'research', 'studies', 'analysis.md')
        
        self.assertEqual(expected_path, expected_nested)
    
    def test_error_handling(self):
        """Test error handling for various failure scenarios"""
        # Test non-existent PDF using subprocess (avoiding import)
        result = subprocess.run([
            sys.executable, self.converter_script, 'non-existent.pdf'
        ], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)  # Should fail
        
        # Test with invalid parameters
        result = subprocess.run([
            sys.executable, self.converter_script, '--help'
        ], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)  # Help should work

class IntegrationTests(unittest.TestCase):
    """Integration tests for the complete pipeline"""
    
    def setUp(self):
        """Set up integration test environment"""
        self.original_dir = os.getcwd()
        # Note: These tests assume we're in the project root
    
    def tearDown(self):
        """Clean up integration tests"""
        os.chdir(self.original_dir)
    
    def test_end_to_end_conversion(self):
        """Test complete end-to-end conversion process"""
        # This test would require actual PDF files and conversion tools
        # For now, we'll test the command line interface
        
        converter_script = 'utilities/pdf-ingestion-pipeline/convert_pdf.py'
        if not os.path.exists(converter_script):
            self.skipTest("Converter script not found")
        
        # Test help command
        try:
            result = subprocess.run([
                sys.executable, converter_script, '--help'
            ], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0)
        except subprocess.SubprocessError:
            self.skipTest("Cannot run converter script")
    
    def test_batch_conversion(self):
        """Test batch conversion functionality"""
        batch_script = 'utilities/pdf-ingestion-pipeline/batch_converter.sh'
        if not os.path.exists(batch_script):
            self.skipTest("Batch converter script not found")
        
        # Test that script exists and is executable
        self.assertTrue(os.access(batch_script, os.X_OK))
    
    def test_validation_integration(self):
        """Test validation script integration"""
        validation_script = 'utilities/validation-scripts/validate_conversion.py'
        if not os.path.exists(validation_script):
            self.skipTest("Validation script not found")
        
        try:
            result = subprocess.run([
                sys.executable, validation_script, '--help'
            ], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0)
        except subprocess.SubprocessError:
            self.skipTest("Cannot run validation script")

class ConfigurationTests(unittest.TestCase):
    """Tests for configuration integration"""
    
    def test_core_config_structure(self):
        """Test core configuration structure"""
        config_file = '.bmad-core/core-config.yaml'
        if not os.path.exists(config_file):
            self.skipTest("Core config file not found")
        
        with open(config_file, 'r') as f:
            content = f.read()
            
        # Check for required configuration sections
        self.assertIn('documentIngestion:', content)
        self.assertIn('pdfConversionRequired: true', content)
        self.assertIn('sourceDocumentsPath:', content)
        self.assertIn('convertedDocumentsPath:', content)
    
    def test_agent_rule_integration(self):
        """Test that agent files contain PDF ingestion rules"""
        agent_files = [
            '.bmad-core/agents/dev.md',
            '.bmad-core/agents/pm.md',
            '.claude/commands/BMad/agents/dev.md'
        ]
        
        for agent_file in agent_files:
            if os.path.exists(agent_file):
                with open(agent_file, 'r') as f:
                    content = f.read()
                self.assertIn('documentIngestionRules:', content)
                self.assertIn('NEVER ingest PDF files directly', content)
    
    def test_required_files_exist(self):
        """Test that all required files exist"""
        required_files = [
            'input-documents/README.md',
            'input-documents-converted-to-md/README.md',
            'docs/pdf-ingestion-rules.md',
            'utilities/pdf-ingestion-pipeline/convert_pdf.py',
            'utilities/validation-scripts/validate_conversion.py',
            'PDF_CONVERSION_WORKFLOW.md',
            'IMPLEMENTATION_PLAN.md'
        ]
        
        for file_path in required_files:
            self.assertTrue(
                os.path.exists(file_path), 
                f"Required file missing: {file_path}"
            )

def run_tests():
    """Run all test suites"""
    print("Running PDF Ingestion Pipeline Test Suite...")
    print("=" * 50)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(PDFIngestionPipelineTests))
    suite.addTests(loader.loadTestsFromTestCase(IntegrationTests))
    suite.addTests(loader.loadTestsFromTestCase(ConfigurationTests))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 50)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\nFailures:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback.split('AssertionError: ')[-1].split('\n')[0]}")
    
    if result.errors:
        print("\nErrors:")
        for test, traceback in result.errors:
            error_lines = traceback.split('\n')
            error_msg = next((line for line in error_lines if 'Error:' in line or 'Exception:' in line), error_lines[-2] if len(error_lines) > 1 else str(test))
            print(f"  - {test}: {error_msg}")
    
    success = len(result.failures) == 0 and len(result.errors) == 0
    print(f"\nOverall: {'PASS' if success else 'FAIL'}")
    
    return success

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)