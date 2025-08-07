#!/usr/bin/env python3
"""
BMAD Data Ingestion Extraction Plan Generator
Implements two-phase extraction workflow with user approval
"""

import os
import sys
import json
import hashlib
import shutil
import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional

class ExtractionPlanGenerator:
    """Generates extraction plans for BMAD data ingestion workflow"""
    
    def __init__(self, source_document: str, target_directory: str = ".ai/extraction-plans"):
        self.source_document = Path(source_document)
        self.target_directory = Path(target_directory)
        self.target_directory.mkdir(parents=True, exist_ok=True)
        
        # Generate plan file name
        document_name = self.source_document.stem
        self.plan_file = self.target_directory / f"{document_name}-extraction-plan.md"
        self.backup_dir = Path(".ai/backups")
        
    def analyze_source_document(self) -> Dict[str, Any]:
        """Analyze source document and identify key data elements"""
        if not self.source_document.exists():
            raise FileNotFoundError(f"Source document not found: {self.source_document}")
        
        try:
            with open(self.source_document, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            raise Exception(f"Failed to read source document: {e}")
        
        # Basic document analysis
        analysis = {
            'document_type': self._identify_document_type(content),
            'content_summary': self._generate_content_summary(content),
            'key_elements': self._identify_key_elements(content),
            'content_length': len(content),
            'line_count': len(content.split('\n')),
            'sections': self._identify_sections(content)
        }
        
        return analysis
    
    def _identify_document_type(self, content: str) -> str:
        """Identify the type of document based on content analysis"""
        content_lower = content.lower()
        
        if 'requirements' in content_lower or 'shall' in content_lower:
            return "Requirements Document"
        elif 'architecture' in content_lower or 'system design' in content_lower:
            return "Architecture Document"
        elif 'user story' in content_lower or 'acceptance criteria' in content_lower:
            return "User Stories Document"
        elif 'api' in content_lower and ('endpoint' in content_lower or 'method' in content_lower):
            return "API Documentation"
        elif 'test' in content_lower and ('case' in content_lower or 'scenario' in content_lower):
            return "Test Documentation"
        elif self.source_document.suffix.lower() == '.md':
            return "Markdown Document"
        elif self.source_document.suffix.lower() in ['.txt', '.doc', '.docx']:
            return "Text Document"
        else:
            return "Unknown Document Type"
    
    def _generate_content_summary(self, content: str) -> str:
        """Generate a 2-3 sentence summary of document content"""
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        
        # Take first few meaningful lines as summary base
        summary_lines = []
        for line in lines[:10]:  # Look at first 10 non-empty lines
            if len(line) > 20 and not line.startswith('#'):  # Skip short lines and headers
                summary_lines.append(line)
                if len(summary_lines) >= 3:
                    break
        
        if summary_lines:
            summary = ' '.join(summary_lines[:3])
            # Truncate if too long
            if len(summary) > 300:
                summary = summary[:297] + "..."
            return summary
        else:
            return f"Document contains {len(lines)} lines of content for analysis and extraction."
    
    def _identify_key_elements(self, content: str) -> List[str]:
        """Identify key data elements that can be extracted"""
        elements = []
        content_lower = content.lower()
        
        # Common element patterns
        if '# ' in content or '## ' in content:
            elements.append("Structured headings and sections")
        
        if 'requirement' in content_lower:
            elements.append("Requirements specifications")
            
        if 'feature' in content_lower:
            elements.append("Feature descriptions")
            
        if 'user' in content_lower and 'story' in content_lower:
            elements.append("User stories and acceptance criteria")
            
        if 'api' in content_lower or 'endpoint' in content_lower:
            elements.append("API specifications")
            
        if 'test' in content_lower:
            elements.append("Testing procedures and cases")
            
        if 'architecture' in content_lower or 'design' in content_lower:
            elements.append("System architecture and design patterns")
            
        if 'data' in content_lower and ('model' in content_lower or 'schema' in content_lower):
            elements.append("Data models and schemas")
        
        # If no specific elements found, provide generic ones
        if not elements:
            elements = [
                "Textual content for documentation",
                "Structured information for organization",
                "Reference material for development"
            ]
        
        return elements[:5]  # Limit to 5 key elements
    
    def _identify_sections(self, content: str) -> List[Dict[str, Any]]:
        """Identify document sections for targeted extraction"""
        sections = []
        lines = content.split('\n')
        
        current_section = None
        section_content = []
        
        for i, line in enumerate(lines):
            # Detect headers (markdown style)
            if line.strip().startswith('#'):
                if current_section:
                    sections.append({
                        'title': current_section,
                        'content': '\n'.join(section_content),
                        'line_start': sections[-1]['line_end'] + 1 if sections else 0,
                        'line_end': i
                    })
                
                current_section = line.strip()
                section_content = []
            else:
                if current_section:
                    section_content.append(line)
        
        # Add final section
        if current_section:
            sections.append({
                'title': current_section,
                'content': '\n'.join(section_content),
                'line_start': sections[-1]['line_end'] + 1 if sections else 0,
                'line_end': len(lines)
            })
        
        return sections
    
    def generate_extraction_operations(self, analysis: Dict[str, Any]) -> Tuple[List[Dict], List[Dict]]:
        """Generate safe and risky extraction operations based on analysis"""
        safe_operations = []
        risky_operations = []
        
        # Generate safe operations (additions/aggregations)
        safe_operations.extend(self._generate_safe_operations(analysis))
        
        # Generate risky operations (modifications/deletions)
        risky_operations.extend(self._generate_risky_operations(analysis))
        
        return safe_operations, risky_operations
    
    def _generate_safe_operations(self, analysis: Dict[str, Any]) -> List[Dict]:
        """Generate safe operations that don't require approval"""
        operations = []
        document_name = self.source_document.stem
        
        # Safe operation: Add extracted content to new section
        operations.append({
            'target_location': f'docs/extracted-content/{document_name}.md',
            'operation': 'CREATE',
            'content_to_add': f'# Extracted Content from {self.source_document.name}\n\n[Extracted content would be placed here]',
            'rationale': 'Create new file with extracted content without modifying existing documentation',
            'dependencies': 'docs/extracted-content/ directory must exist'
        })
        
        # Safe operation: Add to index or catalog
        operations.append({
            'target_location': 'docs/document-index.md',
            'operation': 'ADD',
            'content_to_add': f'- [{self.source_document.name}]({self.source_document}) - {analysis["document_type"]}',
            'rationale': 'Add document reference to project index for better navigation',
            'dependencies': 'Document index file existence'
        })
        
        # Safe operation: Aggregate key elements
        if analysis['key_elements']:
            key_elements_text = '\n'.join(f'- {element}' for element in analysis['key_elements'])
            operations.append({
                'target_location': f'docs/project-data/{document_name}-elements.md',
                'operation': 'CREATE',
                'content_to_add': f'# Key Elements from {self.source_document.name}\n\n{key_elements_text}',
                'rationale': 'Create structured catalog of key data elements for reference',
                'dependencies': 'docs/project-data/ directory must exist'
            })
        
        return operations
    
    def _generate_risky_operations(self, analysis: Dict[str, Any]) -> List[Dict]:
        """Generate risky operations that require user approval"""
        operations = []
        
        # Example risky operation: Modify existing PRD
        if analysis['document_type'] == 'Requirements Document':
            operations.append({
                'target_location': 'docs/prd.md',
                'operation': 'MODIFY',
                'current_content': '[Existing PRD content would be analyzed here]',
                'proposed_content': '[Merged content with new requirements]',
                'rationale': 'Integrate new requirements with existing PRD structure',
                'risk_assessment': 'MEDIUM - Could overwrite existing requirements or create conflicts',
                'approval_status': 'PENDING'
            })
        
        # Example risky operation: Restructure documentation
        operations.append({
            'target_location': 'docs/',
            'operation': 'RESTRUCTURE',
            'current_content': '[Current documentation structure]',
            'proposed_content': '[New structure incorporating extracted content]',
            'rationale': 'Reorganize documentation to better integrate extracted information',
            'risk_assessment': 'HIGH - Could disrupt existing documentation organization',
            'approval_status': 'PENDING'
        })
        
        return operations
    
    def generate_plan_file(self, analysis: Dict[str, Any], safe_ops: List[Dict], risky_ops: List[Dict]) -> str:
        """Generate the extraction plan markdown file"""
        document_name = self.source_document.name
        
        plan_content = f"""# {document_name} Extraction Plan

## Source Document Analysis
- **Document Type**: {analysis['document_type']}
- **Content Summary**: {analysis['content_summary']}
- **Key Data Elements Identified**: 
"""
        
        for element in analysis['key_elements']:
            plan_content += f"  - {element}\n"
        
        plan_content += "\n## Proposed Extractions\n\n"
        
        # Safe operations section
        plan_content += "### SAFE OPERATIONS (Auto-Approved)\n#### Information Aggregations\n"
        
        for i, op in enumerate(safe_ops, 1):
            plan_content += f"""
{i}. **Target Location**: {op['target_location']}
   **Operation**: {op['operation']}
   **Content to Add**:
   ```
   {op['content_to_add']}
   ```
   **Rationale**: {op['rationale']}
   **Dependencies**: {op['dependencies']}
"""
        
        # Risky operations section
        plan_content += "\n### REQUIRES USER APPROVAL\n#### Information Modifications\n"
        
        for i, op in enumerate(risky_ops, 1):
            plan_content += f"""
{i}. **Target Location**: {op['target_location']}
   **Operation**: {op['operation']}
   **Current Content**:
   ```
   {op['current_content']}
   ```
   **Proposed Content**:
   ```
   {op['proposed_content']}
   ```
   **Rationale**: {op['rationale']}
   **Risk Assessment**: {op['risk_assessment']}
   **Approval Status**: {op['approval_status']}
"""
        
        # Execution summary
        plan_content += f"""
## Execution Summary
- **Safe Operations**: {len(safe_ops)} additions/aggregations
- **Approval Required**: {len(risky_ops)} modifications/deletions
- **Estimated Completion Time**: {self._estimate_completion_time(safe_ops, risky_ops)}

## Execution Commands
```bash
# Commands to execute this plan (generated automatically)
python3 utilities/extraction-pipeline/execute_extraction_plan.py {self.plan_file}
```
"""
        
        return plan_content
    
    def _estimate_completion_time(self, safe_ops: List[Dict], risky_ops: List[Dict]) -> str:
        """Estimate completion time for operations"""
        total_ops = len(safe_ops) + len(risky_ops)
        
        if total_ops <= 3:
            return "2-5 minutes"
        elif total_ops <= 6:
            return "5-10 minutes"  
        elif total_ops <= 10:
            return "10-20 minutes"
        else:
            return "20+ minutes"
    
    def save_plan_file(self, plan_content: str) -> str:
        """Save extraction plan to file"""
        try:
            with open(self.plan_file, 'w', encoding='utf-8') as f:
                f.write(plan_content)
            return str(self.plan_file)
        except Exception as e:
            raise Exception(f"Failed to save plan file: {e}")
    
    def generate_extraction_plan(self) -> str:
        """Main method to generate complete extraction plan"""
        print(f"Analyzing source document: {self.source_document}")
        
        # Phase 1: Analyze source document
        analysis = self.analyze_source_document()
        print(f"Document type identified: {analysis['document_type']}")
        
        # Phase 2: Generate operations
        safe_ops, risky_ops = self.generate_extraction_operations(analysis)
        print(f"Generated {len(safe_ops)} safe operations and {len(risky_ops)} operations requiring approval")
        
        # Phase 3: Generate plan file
        plan_content = self.generate_plan_file(analysis, safe_ops, risky_ops)
        plan_file_path = self.save_plan_file(plan_content)
        
        print(f"✓ Extraction plan generated: {plan_file_path}")
        print(f"  - Safe operations: {len(safe_ops)}")
        print(f"  - Approval required: {len(risky_ops)}")
        
        return plan_file_path

def main():
    """Command line interface for extraction plan generator"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate BMAD extraction plan for source document')
    parser.add_argument('source_document', help='Path to source document')
    parser.add_argument('--target-dir', default='.ai/extraction-plans', 
                       help='Target directory for extraction plans')
    
    args = parser.parse_args()
    
    try:
        generator = ExtractionPlanGenerator(args.source_document, args.target_dir)
        plan_file = generator.generate_extraction_plan()
        
        print(f"\n✅ Extraction plan ready for review:")
        print(f"   {plan_file}")
        print(f"\n📋 Next steps:")
        print(f"   1. Review the extraction plan")
        print(f"   2. Approve any operations marked as 'PENDING'")
        print(f"   3. Execute the plan with: execute-extraction-plan {plan_file}")
        
    except Exception as e:
        print(f"❌ Error generating extraction plan: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()