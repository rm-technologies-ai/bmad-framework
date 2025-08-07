#!/usr/bin/env python3
"""
PDF Conversion Validation Script
Validates the quality and completeness of PDF-to-Markdown conversions
"""

import os
import sys
import argparse
from pathlib import Path

def validate_markdown_file(md_path):
    """
    Validate a converted markdown file.
    
    Args:
        md_path (str): Path to markdown file
    
    Returns:
        dict: Validation results with scores and issues
    """
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
    
    # Basic content validation
    if not content.strip():
        results['valid'] = False
        results['issues'].append('File is empty')
        return results
    
    # Content quality checks
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
    
    # Consider it invalid if score is too low
    if score < 40:
        results['valid'] = False
        results['issues'].append('Content quality score too low')
    
    return results

def validate_conversion_pair(pdf_path, md_path):
    """
    Validate a PDF/Markdown conversion pair.
    
    Args:
        pdf_path (str): Path to source PDF
        md_path (str): Path to converted Markdown
    
    Returns:
        dict: Validation results
    """
    results = {
        'pdf_exists': os.path.exists(pdf_path),
        'md_exists': os.path.exists(md_path),
        'md_validation': None,
        'overall_valid': False
    }
    
    if not results['pdf_exists']:
        return results
    
    if results['md_exists']:
        results['md_validation'] = validate_markdown_file(md_path)
        results['overall_valid'] = results['md_validation']['valid']
    
    return results

def find_conversion_pairs():
    """
    Find all PDF/Markdown conversion pairs in the project.
    
    Returns:
        list: List of (pdf_path, md_path) tuples
    """
    pairs = []
    input_dir = Path('input-documents')
    converted_dir = Path('input-documents-converted-to-md')
    
    if not input_dir.exists():
        return pairs
    
    # Find all PDFs
    for pdf_file in input_dir.rglob('*.pdf'):
        relative_path = pdf_file.relative_to(input_dir)
        base_name = relative_path.stem
        
        # Look for converted versions
        converted_base = converted_dir / relative_path.parent
        
        if converted_base.exists():
            # Find latest version
            md_files = list(converted_base.glob(f'{base_name}*.md'))
            if md_files:
                # Sort to get latest version
                md_files.sort(key=lambda x: x.name)
                latest_md = md_files[-1]
                pairs.append((str(pdf_file), str(latest_md)))
    
    return pairs

def main():
    parser = argparse.ArgumentParser(description='Validate PDF conversions')
    parser.add_argument('--file', help='Validate specific markdown file')
    parser.add_argument('--all', action='store_true', help='Validate all conversions')
    parser.add_argument('--summary', action='store_true', help='Show summary only')
    
    args = parser.parse_args()
    
    if args.file:
        # Validate single file
        results = validate_markdown_file(args.file)
        
        print(f"Validation Results for: {args.file}")
        print(f"Valid: {results['valid']}")
        print(f"Score: {results['score']}/{results['max_score']}")
        
        if results['issues']:
            print("\nIssues:")
            for issue in results['issues']:
                print(f"  ✗ {issue}")
        
        if results['warnings']:
            print("\nWarnings:")
            for warning in results['warnings']:
                print(f"  ⚠ {warning}")
        
        sys.exit(0 if results['valid'] else 1)
    
    elif args.all:
        # Validate all conversion pairs
        pairs = find_conversion_pairs()
        
        if not pairs:
            print("No conversion pairs found")
            sys.exit(0)
        
        total_pairs = len(pairs)
        valid_pairs = 0
        
        print(f"Validating {total_pairs} conversion pairs...\n")
        
        for pdf_path, md_path in pairs:
            pair_results = validate_conversion_pair(pdf_path, md_path)
            
            if not args.summary:
                print(f"PDF: {pdf_path}")
                print(f"MD:  {md_path}")
                
                if pair_results['overall_valid']:
                    print("✓ Valid conversion")
                    valid_pairs += 1
                else:
                    print("✗ Invalid conversion")
                    if pair_results['md_validation']:
                        for issue in pair_results['md_validation']['issues']:
                            print(f"  - {issue}")
                print()
            else:
                if pair_results['overall_valid']:
                    valid_pairs += 1
        
        # Summary
        print(f"\nValidation Summary:")
        print(f"Total pairs: {total_pairs}")
        print(f"Valid conversions: {valid_pairs}")
        print(f"Invalid conversions: {total_pairs - valid_pairs}")
        print(f"Success rate: {(valid_pairs / total_pairs * 100):.1f}%")
        
        sys.exit(0 if valid_pairs == total_pairs else 1)
    
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()