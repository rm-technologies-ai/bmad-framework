#!/usr/bin/env python3
"""
PDF Ingestion Pipeline - Main Conversion Script
Wrapper for the PDF-to-MD converter with BMAD-specific logic
"""

import sys
import os
import glob
import re
import subprocess
from pathlib import Path

def get_next_version_path(base_path, converted_dir):
    """
    Determine the next version path for a converted markdown file.
    
    Args:
        base_path (str): Original PDF path
        converted_dir (str): Converted documents directory
    
    Returns:
        str: Path for the new markdown file with appropriate version
    """
    pdf_path = Path(base_path)
    relative_path = pdf_path.relative_to('input-documents') if 'input-documents' in str(pdf_path) else pdf_path
    
    # Base name without extension
    base_name = relative_path.stem
    parent_dir = relative_path.parent
    
    # Target directory in converted folder
    target_dir = Path(converted_dir) / parent_dir
    target_dir.mkdir(parents=True, exist_ok=True)
    
    # Check for existing versions
    existing_files = list(target_dir.glob(f"{base_name}*.md"))
    
    if not existing_files:
        # First conversion
        return str(target_dir / f"{base_name}.md")
    
    # Extract version numbers from existing files
    version_pattern = re.compile(rf"{re.escape(base_name)}_v(\d+)\.md$")
    versions = []
    
    for file_path in existing_files:
        match = version_pattern.search(file_path.name)
        if match:
            versions.append(int(match.group(1)))
        elif file_path.name == f"{base_name}.md":
            versions.append(1)  # Base version counts as v1
    
    if not versions:
        return str(target_dir / f"{base_name}.md")
    
    next_version = max(versions) + 1
    return str(target_dir / f"{base_name}_v{next_version}.md")

def get_latest_version_path(base_path, converted_dir):
    """
    Get the path to the latest version of a converted file.
    
    Args:
        base_path (str): Original PDF path or base name
        converted_dir (str): Converted documents directory
    
    Returns:
        str: Path to latest version, or None if no conversion exists
    """
    if base_path.endswith('.pdf'):
        pdf_path = Path(base_path)
        relative_path = pdf_path.relative_to('input-documents') if 'input-documents' in str(pdf_path) else pdf_path
        base_name = relative_path.stem
        parent_dir = relative_path.parent
    else:
        # Handle case where base_path is already a base name
        parts = base_path.split('/')
        base_name = Path(parts[-1]).stem
        parent_dir = '/'.join(parts[:-1]) if len(parts) > 1 else ''
    
    target_dir = Path(converted_dir) / parent_dir
    
    if not target_dir.exists():
        return None
    
    # Find all versions
    existing_files = list(target_dir.glob(f"{base_name}*.md"))
    
    if not existing_files:
        return None
    
    # Find highest version
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

def convert_pdf(pdf_path, force_reconvert=False):
    """
    Convert PDF to Markdown using the conversion pipeline.
    
    Args:
        pdf_path (str): Path to PDF file
        force_reconvert (bool): Force reconversion even if MD exists
    
    Returns:
        str: Path to converted markdown file, or None if failed
    """
    converted_dir = "input-documents-converted-to-md"
    converter_script = "utilities/pdf-to-md-converter/convert_pdf_to_md.py"
    
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found: {pdf_path}")
        return None
    
    if not os.path.exists(converter_script):
        print(f"Error: Converter script not found: {converter_script}")
        return None
    
    # Check if conversion already exists
    if not force_reconvert:
        existing_path = get_latest_version_path(pdf_path, converted_dir)
        if existing_path and os.path.exists(existing_path):
            print(f"✓ Using existing conversion: {existing_path}")
            return existing_path
    
    # Determine output path
    output_path = get_next_version_path(pdf_path, converted_dir)
    
    print(f"Converting: {pdf_path} -> {output_path}")
    
    # Run conversion
    try:
        result = subprocess.run([
            sys.executable, converter_script, pdf_path, output_path
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✓ Conversion successful: {output_path}")
            return output_path
        else:
            print(f"✗ Conversion failed: {result.stderr}")
            return None
            
    except Exception as e:
        print(f"✗ Conversion error: {e}")
        return None

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='BMAD PDF Ingestion Pipeline')
    parser.add_argument('pdf_path', help='Path to PDF file')
    parser.add_argument('--force', action='store_true', help='Force reconversion')
    parser.add_argument('--latest', action='store_true', help='Get latest version path only')
    
    args = parser.parse_args()
    
    if args.latest:
        latest_path = get_latest_version_path(args.pdf_path, "input-documents-converted-to-md")
        if latest_path:
            print(latest_path)
            sys.exit(0)
        else:
            print(f"No conversion found for: {args.pdf_path}")
            sys.exit(1)
    
    result_path = convert_pdf(args.pdf_path, args.force)
    sys.exit(0 if result_path else 1)

if __name__ == "__main__":
    main()