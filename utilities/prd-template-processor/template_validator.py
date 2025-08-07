#!/usr/bin/env python3
"""
PRD Template Validator
Validates PRD files against the mandatory template structure
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field

@dataclass
class ValidationResult:
    """Result of template validation"""
    is_valid: bool
    score: float
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    missing_sections: List[str] = field(default_factory=list)
    extra_sections: List[str] = field(default_factory=list)
    section_analysis: Dict[str, dict] = field(default_factory=dict)

@dataclass
class TemplateSection:
    """Expected template section"""
    title: str
    level: int
    required: bool = True
    order: int = 0

class PRDTemplateValidator:
    """Validates PRD files against template structure"""
    
    def __init__(self, template_path: str):
        self.template_path = Path(template_path)
        self.expected_sections = self._load_template_structure()
    
    def _load_template_structure(self) -> List[TemplateSection]:
        """Load expected section structure from template"""
        try:
            with open(self.template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
            return self._parse_template_structure(template_content)
        except FileNotFoundError:
            raise FileNotFoundError(f"Template file not found: {self.template_path}")
    
    def _parse_template_structure(self, content: str) -> List[TemplateSection]:
        """Parse template to extract expected section structure"""
        # Define expected sections based on the actual PRD template structure
        expected_sections = [
            TemplateSection("MASTER PRD CLASSIFICATION GUIDE", 1, True, 1),
            TemplateSection("OPTIMAL PRD STRUCTURE FOR ATLAS-DS", 2, True, 2),
            TemplateSection("1. DOCUMENT FOUNDATION & CONTEXT", 3, True, 3),
            TemplateSection("2. EXECUTIVE SUMMARY & STRATEGIC VISION", 3, True, 4),
            TemplateSection("3. BUSINESS CONTEXT & MARKET ANALYSIS", 3, True, 5),
            TemplateSection("4. USER RESEARCH & EXPERIENCE DESIGN", 3, True, 6),
            TemplateSection("5. FUNCTIONAL REQUIREMENTS & FEATURE SPECIFICATIONS", 3, True, 7),
            TemplateSection("6. NON-FUNCTIONAL REQUIREMENTS (NFRS)", 3, True, 8),
            TemplateSection("7. AI/ML INTEGRATION & ADVANCED CAPABILITIES", 3, True, 9),
            TemplateSection("8. TECHNICAL ARCHITECTURE & IMPLEMENTATION", 3, True, 10),
            TemplateSection("9. SUCCESS METRICS & PERFORMANCE MEASUREMENT", 3, True, 11),
            TemplateSection("10. DEVELOPMENT METHODOLOGY & PROJECT PLANNING", 3, True, 12),
            TemplateSection("11. QUALITY ASSURANCE & TESTING STRATEGY", 3, True, 13),
            TemplateSection("12. LAUNCH STRATEGY & GO-TO-MARKET", 3, True, 14),
            TemplateSection("13. GOVERNANCE, COMPLIANCE & RISK MANAGEMENT", 3, True, 15),
            TemplateSection("14. DEPENDENCIES, ASSUMPTIONS & CONSTRAINTS", 3, True, 16),
            TemplateSection("15. SUPPORTING DOCUMENTATION & APPENDICES", 3, True, 17),
            TemplateSection("DOCUMENT PROCESSING WORKFLOW FOR ATLAS-DS", 2, True, 18),
            TemplateSection("ATLAS-DS SPECIFIC CONSIDERATIONS", 2, True, 19),
        ]
        
        return expected_sections
    
    def validate_prd_file(self, prd_file_path: str) -> ValidationResult:
        """
        Validate PRD file against template structure
        
        Args:
            prd_file_path: Path to PRD file to validate
            
        Returns:
            ValidationResult with detailed analysis
        """
        prd_path = Path(prd_file_path)
        
        if not prd_path.exists():
            return ValidationResult(
                is_valid=False,
                score=0.0,
                errors=[f"PRD file not found: {prd_file_path}"]
            )
        
        try:
            with open(prd_path, 'r', encoding='utf-8') as f:
                prd_content = f.read()
        except Exception as e:
            return ValidationResult(
                is_valid=False,
                score=0.0,
                errors=[f"Error reading PRD file: {e}"]
            )
        
        return self._perform_validation(prd_content, str(prd_path))
    
    def _perform_validation(self, content: str, file_path: str) -> ValidationResult:
        """Perform comprehensive validation of PRD content"""
        result = ValidationResult(is_valid=True, score=0.0)
        
        # Extract sections from PRD content
        actual_sections = self._extract_sections(content)
        
        # Validate structure
        self._validate_structure(actual_sections, result)
        
        # Validate content
        self._validate_content(content, result)
        
        # Validate metadata
        self._validate_metadata(content, result)
        
        # Calculate overall score
        result.score = self._calculate_score(result)
        result.is_valid = result.score >= 0.8 and len(result.errors) == 0
        
        return result
    
    def _extract_sections(self, content: str) -> List[Tuple[str, int]]:
        """Extract section headings and their levels from content"""
        sections = []
        
        # Find all markdown headings
        heading_pattern = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)
        
        for match in heading_pattern.finditer(content):
            level = len(match.group(1))
            title = match.group(2).strip()
            sections.append((title, level))
        
        return sections
    
    def _validate_structure(self, actual_sections: List[Tuple[str, int]], result: ValidationResult):
        """Validate section structure against template"""
        actual_titles = [section[0] for section in actual_sections]
        expected_titles = [section.title for section in self.expected_sections]
        
        # Check for missing required sections
        for expected in self.expected_sections:
            if expected.required and expected.title not in actual_titles:
                result.missing_sections.append(expected.title)
                result.errors.append(f"Missing required section: {expected.title}")
        
        # Check for unexpected sections
        for actual_title, level in actual_sections:
            if actual_title not in expected_titles and level <= 3:  # Only flag high-level unexpected sections
                result.extra_sections.append(actual_title)
                result.warnings.append(f"Unexpected section found: {actual_title}")
        
        # Analyze section order
        self._validate_section_order(actual_sections, result)
        
        # Analyze individual sections
        for actual_title, level in actual_sections:
            result.section_analysis[actual_title] = {
                'level': level,
                'expected': actual_title in expected_titles,
                'content_length': 0  # Would be populated by content analysis
            }
    
    def _validate_section_order(self, actual_sections: List[Tuple[str, int]], result: ValidationResult):
        """Validate that sections appear in expected order"""
        expected_order = {section.title: section.order for section in self.expected_sections}
        
        previous_order = 0
        for title, level in actual_sections:
            if title in expected_order:
                current_order = expected_order[title]
                if current_order < previous_order:
                    result.warnings.append(f"Section '{title}' appears out of expected order")
                previous_order = current_order
    
    def _validate_content(self, content: str, result: ValidationResult):
        """Validate content quality and completeness"""
        lines = content.split('\n')
        
        # Check for empty sections
        current_section = None
        section_content = []
        
        for line in lines:
            if re.match(r'^#{1,6}\s+', line):
                # Process previous section
                if current_section and len(section_content) < 3:
                    result.warnings.append(f"Section '{current_section}' appears to have minimal content")
                
                # Start new section
                current_section = line.strip('#').strip()
                section_content = []
            else:
                if line.strip():  # Non-empty line
                    section_content.append(line)
        
        # Check final section
        if current_section and len(section_content) < 3:
            result.warnings.append(f"Section '{current_section}' appears to have minimal content")
        
        # Validate specific content requirements
        self._validate_specific_requirements(content, result)
    
    def _validate_specific_requirements(self, content: str, result: ValidationResult):
        """Validate specific content requirements for PRD sections"""
        content_lower = content.lower()
        
        # Check for classification guide indicators
        if "content aggregation focus" not in content_lower:
            result.warnings.append("Missing 'Content Aggregation Focus' indicators in sections")
        
        # Check for required terminology
        required_terms = ["functional requirements", "non-functional requirements", "technical architecture", "success metrics"]
        for term in required_terms:
            if term not in content_lower:
                result.warnings.append(f"Missing expected terminology: {term}")
        
        # Check for Atlas-DS specific content
        atlas_terms = ["atlas", "data science", "fedramp", "compliance"]
        atlas_found = any(term in content_lower for term in atlas_terms)
        if not atlas_found:
            result.warnings.append("Content may not be specific to Atlas-DS project context")
    
    def _validate_metadata(self, content: str, result: ValidationResult):
        """Validate metadata and template compliance"""
        # Check for version control metadata
        if "<!--" not in content or "PRD Version:" not in content:
            result.warnings.append("Missing version control metadata header")
        
        # Check for template reference
        if "templates/PRD-template.md" not in content:
            result.warnings.append("Missing reference to source template")
        
        # Check for generation timestamp
        if not re.search(r'Generated:\s*\d{4}-\d{2}-\d{2}', content):
            result.warnings.append("Missing generation timestamp")
    
    def _calculate_score(self, result: ValidationResult) -> float:
        """Calculate overall validation score"""
        score = 1.0
        
        # Deduct for errors (major issues)
        score -= len(result.errors) * 0.2
        
        # Deduct for missing required sections
        score -= len(result.missing_sections) * 0.15
        
        # Deduct for warnings (minor issues)
        score -= len(result.warnings) * 0.05
        
        # Bonus for having all expected sections
        expected_count = len([s for s in self.expected_sections if s.required])
        actual_count = expected_count - len(result.missing_sections)
        if actual_count == expected_count:
            score += 0.1
        
        return max(0.0, min(1.0, score))  # Clamp between 0 and 1
    
    def validate_template_compliance(self, prd_content: str) -> Dict[str, bool]:
        """Quick compliance check against template structure"""
        compliance = {
            'has_required_sections': True,
            'follows_structure': True,
            'has_metadata': True,
            'has_content_focus': True,
            'has_atlas_context': True
        }
        
        content_lower = prd_content.lower()
        
        # Check required sections
        required_section_indicators = [
            "document foundation",
            "executive summary",
            "business context",
            "functional requirements",
            "non-functional requirements",
            "technical architecture"
        ]
        
        for indicator in required_section_indicators:
            if indicator not in content_lower:
                compliance['has_required_sections'] = False
                break
        
        # Check structure
        heading_count = len(re.findall(r'^#{1,6}\s+', prd_content, re.MULTILINE))
        if heading_count < 15:  # Should have at least 15 major sections
            compliance['follows_structure'] = False
        
        # Check metadata
        if "<!--" not in prd_content or "PRD Version:" not in prd_content:
            compliance['has_metadata'] = False
        
        # Check content focus
        if "content aggregation focus" not in content_lower:
            compliance['has_content_focus'] = False
        
        # Check Atlas context
        atlas_indicators = ["atlas", "data science", "project lion"]
        if not any(indicator in content_lower for indicator in atlas_indicators):
            compliance['has_atlas_context'] = False
        
        return compliance
    
    def generate_validation_report(self, validation_result: ValidationResult, file_path: str = "") -> str:
        """Generate human-readable validation report"""
        report = []
        
        report.append("# PRD Template Validation Report")
        report.append(f"**File**: {file_path}")
        report.append(f"**Template**: {self.template_path}")
        report.append(f"**Validation Date**: {Path().cwd()}")  # Would use actual timestamp
        report.append("")
        
        # Overall result
        status = "✅ VALID" if validation_result.is_valid else "❌ INVALID"
        report.append(f"## Overall Result: {status}")
        report.append(f"**Score**: {validation_result.score:.2f}/1.00")
        report.append("")
        
        # Errors
        if validation_result.errors:
            report.append("## ❌ Errors (Must Fix)")
            for error in validation_result.errors:
                report.append(f"- {error}")
            report.append("")
        
        # Warnings
        if validation_result.warnings:
            report.append("## ⚠️ Warnings (Should Fix)")
            for warning in validation_result.warnings:
                report.append(f"- {warning}")
            report.append("")
        
        # Missing sections
        if validation_result.missing_sections:
            report.append("## Missing Required Sections")
            for section in validation_result.missing_sections:
                report.append(f"- {section}")
            report.append("")
        
        # Extra sections
        if validation_result.extra_sections:
            report.append("## Unexpected Sections")
            for section in validation_result.extra_sections:
                report.append(f"- {section}")
            report.append("")
        
        # Section analysis
        if validation_result.section_analysis:
            report.append("## Section Analysis")
            for section, analysis in validation_result.section_analysis.items():
                expected_icon = "✅" if analysis['expected'] else "❓"
                report.append(f"- {expected_icon} **{section}** (Level {analysis['level']})")
            report.append("")
        
        # Recommendations
        report.append("## Recommendations")
        if validation_result.is_valid:
            report.append("✅ PRD structure is compliant with template requirements.")
        else:
            report.append("❌ PRD requires corrections before approval:")
            if validation_result.missing_sections:
                report.append("  - Add missing required sections")
            if validation_result.errors:
                report.append("  - Fix structural errors")
            if len(validation_result.warnings) > 5:
                report.append("  - Address content warnings")
        
        return "\n".join(report)


def main():
    """CLI interface for template validation"""
    import argparse
    
    parser = argparse.ArgumentParser(description="PRD Template Validator")
    parser.add_argument("--template", required=True, help="Path to PRD template file")
    parser.add_argument("--prd-file", required=True, help="PRD file to validate")
    parser.add_argument("--output-report", help="Output validation report to file")
    parser.add_argument("--json-output", action='store_true', help="Output results as JSON")
    
    args = parser.parse_args()
    
    try:
        validator = PRDTemplateValidator(args.template)
        result = validator.validate_prd_file(args.prd_file)
        
        if args.json_output:
            # Convert dataclass to dict for JSON output
            output = {
                'is_valid': result.is_valid,
                'score': result.score,
                'errors': result.errors,
                'warnings': result.warnings,
                'missing_sections': result.missing_sections,
                'extra_sections': result.extra_sections,
                'section_analysis': result.section_analysis
            }
            print(json.dumps(output, indent=2))
        else:
            report = validator.generate_validation_report(result, args.prd_file)
            
            if args.output_report:
                with open(args.output_report, 'w', encoding='utf-8') as f:
                    f.write(report)
                print(f"Validation report written to: {args.output_report}")
            else:
                print(report)
        
        # Exit with non-zero code if validation failed
        return 0 if result.is_valid else 1
        
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    exit(main())