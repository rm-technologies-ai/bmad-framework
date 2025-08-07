#!/usr/bin/env python3
"""
Convert NIST 800-53 security controls CSV to structured Markdown format.
Handles the MVP Security Scope Analysis document for BMad processing.
"""

import csv
import sys
from pathlib import Path

def clean_text(text):
    """Clean and format text for markdown display"""
    if not text or text.strip() == '':
        return ''
    return text.strip().replace('\n', ' ').replace('\r', '')

def convert_csv_to_markdown(csv_file, output_file):
    """Convert security controls CSV to structured markdown"""
    
    # Read CSV data
    controls = []
    with open(csv_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            controls.append(row)
    
    # Create markdown content
    markdown_lines = [
        "# MVP Security - Scope Analysis - Draft Classifications",
        "",
        "**Source:** `MVP Security - Scope Analysis - Draft Classifications - 2025-07-31.csv`",
        f"**Converted:** {Path(__file__).name}",
        "**Total Controls:** {}".format(len(controls)),
        "",
        "## NIST 800-53 Revision 5 Security Controls Analysis",
        "",
        "This document contains the complete analysis of NIST 800-53 Rev 5 moderate baseline security controls for the Atlas Data Science Project Lion MVP. Controls are classified using the three-level methodology defined in the Security Requirements Classification document.",
        "",
        "### Control Classification Legend",
        "",
        "- **In Scope:** Indicates if control applies to MVP implementation",  
        "- **MVP Requirement:** Specific implementation requirements and acceptance criteria",
        "- **Control Type:** Classification level (Inherited, Customer-Provided, Developer-Implemented)",
        "- **Baseline:** Security control baseline applicability (Low, Moderate, High)",
        "",
        "---",
        "",
        "## Security Controls Inventory",
        ""
    ]
    
    # Group controls by family
    control_families = {}
    for control in controls:
        identifier = control.get('Control Identifier', '').strip()
        if identifier:
            family = identifier.split('-')[0] if '-' in identifier else 'Other'
            if family not in control_families:
                control_families[family] = []
            control_families[family].append(control)
    
    # Process each family
    for family in sorted(control_families.keys()):
        family_controls = control_families[family]
        
        markdown_lines.extend([
            f"### {family} - Family Controls ({len(family_controls)} controls)",
            ""
        ])
        
        # Create table for this family
        table_header = [
            "| Control | Name | In Scope | MVP Requirement | Baseline |",
            "|---------|------|----------|-----------------|----------|"
        ]
        markdown_lines.extend(table_header)
        
        for control in family_controls:
            identifier = clean_text(control.get('Control Identifier', ''))
            name = clean_text(control.get('Control (or Control Enhancement) Name', ''))
            in_scope = clean_text(control.get('In Scope', ''))
            mvp_req = clean_text(control.get('MVP Requirement and Acceptance Criteria', ''))
            moderate = control.get('Security Control Baseline - Moderate', '').strip()
            
            # Truncate long text for table readability
            if len(name) > 50:
                name = name[:47] + "..."
            if len(mvp_req) > 80:
                mvp_req = mvp_req[:77] + "..."
            
            baseline = "✓" if moderate.lower() == 'x' else ""
            
            row = f"| `{identifier}` | {name} | {in_scope} | {mvp_req} | {baseline} |"
            markdown_lines.append(row)
        
        markdown_lines.append("")  # Add spacing between families
    
    # Add detailed control specifications section
    markdown_lines.extend([
        "---",
        "",
        "## Detailed Control Specifications",
        "",
        "*Note: Due to document length, full control text and discussion are preserved in original CSV format. Key implementation requirements are extracted above in the family tables.*",
        "",
        "### Developer-Implemented Controls Summary",
        "",
        "For BMad agent processing, the following control families require active development implementation:",
        ""
    ])
    
    # Count moderate baseline controls by family
    moderate_families = {}
    for control in controls:
        identifier = control.get('Control Identifier', '').strip()
        moderate = control.get('Security Control Baseline - Moderate', '').strip()
        in_scope = clean_text(control.get('In Scope', '')).lower()
        mvp_req = clean_text(control.get('MVP Requirement and Acceptance Criteria', ''))
        
        if moderate.lower() == 'x' and identifier:
            family = identifier.split('-')[0]
            if family not in moderate_families:
                moderate_families[family] = {'total': 0, 'in_scope': 0, 'with_requirements': 0}
            moderate_families[family]['total'] += 1
            if in_scope in ['yes', 'true', '1', 'x']:
                moderate_families[family]['in_scope'] += 1
            if mvp_req:
                moderate_families[family]['with_requirements'] += 1
    
    # Summary table
    summary_header = [
        "| Family | Total Controls | In Scope | With MVP Requirements | Priority |",
        "|--------|----------------|----------|-----------------------|----------|"
    ]
    markdown_lines.extend(summary_header)
    
    for family in sorted(moderate_families.keys()):
        stats = moderate_families[family]
        priority = "High" if stats['with_requirements'] > 0 else "Medium" if stats['in_scope'] > 0 else "Low"
        
        row = f"| {family} | {stats['total']} | {stats['in_scope']} | {stats['with_requirements']} | {priority} |"
        markdown_lines.append(row)
    
    # Footer
    markdown_lines.extend([
        "",
        "---",
        "",
        "## Integration Notes",
        "",
        "### BMad Agent Processing",
        "- Use `/analyst` for security requirements analysis and gap identification",
        "- Use `/architect` for security architecture validation against controls", 
        "- Use `/pm` for security story prioritization and sprint planning",
        "- Use `/dev` for security control implementation in Project Lion components",
        "",
        "### Project Lion Component Mapping",
        "Security controls directly impact:",
        "- **Edge Connector:** Customer VPC isolation, IAM permissions, encryption",
        "- **Ingestion Gateway:** Authentication, authorization, audit logging", 
        "- **Metadata Catalog:** Data classification, access controls, audit trails",
        "- **Policy Engine:** RBAC, ABAC implementation requirements",
        "- **Search & Discovery:** Tenant isolation, field-level security",
        "",
        f"**Total Controls Analyzed:** {len(controls)}",
        f"**Moderate Baseline Controls:** {sum(1 for c in controls if c.get('Security Control Baseline - Moderate', '').strip().lower() == 'x')}",
        f"**Control Families:** {len(control_families)}",
        "",
        "*Generated from CSV export for BMad-Method security requirements processing*"
    ])
    
    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(markdown_lines))
    
    print(f"✅ Converted {len(controls)} security controls to {output_file}")
    print(f"📊 Found {len(control_families)} control families")
    print(f"🎯 {len(moderate_families)} families in moderate baseline")

if __name__ == "__main__":
    csv_file = "/mnt/d/repos/atlas-repos/bmad-framework/input-documents/security-requirements/MVP Security - Scope Analysis - Draft Classifications - 2025-07-31.csv"
    output_file = "/mnt/d/repos/atlas-repos/bmad-framework/input-documents-converted-to-md/security-requirements/MVP Security - Scope Analysis - Draft Classifications - 2025-07-31.md"
    
    try:
        convert_csv_to_markdown(csv_file, output_file)
    except Exception as e:
        print(f"❌ Conversion failed: {e}")
        sys.exit(1)