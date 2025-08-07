#!/usr/bin/env python3
"""
PRD Template Classification System
Maps content to predefined PRD template sections for consistent structure enforcement
"""

import re
import json
import yaml
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from pathlib import Path

@dataclass
class TemplateSection:
    """Represents a section in the PRD template"""
    id: str
    title: str
    content_focus: str
    keywords: List[str] = field(default_factory=list)
    triggers: List[str] = field(default_factory=list)
    content_types: List[str] = field(default_factory=list)
    priority: int = 0

@dataclass
class ClassificationResult:
    """Result of content classification to template sections"""
    section_id: str
    confidence: float
    matched_keywords: List[str]
    reasoning: str
    content_snippet: str

@dataclass
class UncategorizedContent:
    """Content that couldn't be classified to any template section"""
    content: str
    source_file: str
    attempted_sections: List[str]
    reasoning: str
    suggestions: List[str]

class PRDTemplateClassificationSystem:
    """Classification system for mapping content to PRD template sections"""
    
    def __init__(self, template_path: str):
        self.template_path = Path(template_path)
        self.sections: Dict[str, TemplateSection] = {}
        self.uncategorized_content: List[UncategorizedContent] = []
        self._load_template()
        self._initialize_classification_system()
    
    def _load_template(self):
        """Load and parse the PRD template structure"""
        try:
            with open(self.template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
            self._parse_template_sections(template_content)
        except FileNotFoundError:
            raise FileNotFoundError(f"PRD template not found at {self.template_path}")
        except Exception as e:
            raise Exception(f"Error loading PRD template: {e}")
    
    def _parse_template_sections(self, content: str):
        """Parse template content to extract section structure"""
        # Extract sections based on the specific template format
        sections_data = {
            "document_foundation_context": TemplateSection(
                id="document_foundation_context",
                title="Document Foundation & Context",
                content_focus="Document control, definitions, compliance frameworks",
                keywords=["document", "version", "control", "definitions", "glossary", "compliance", "standards", "framework"],
                triggers=["FedRAMP", "ICAM", "FGAC", "STIG", "PKI", "STANAG", "UCO", "JSON-LD", "version control"],
                content_types=["document_control", "definitions", "standards_references", "change_logs"],
                priority=1
            ),
            "executive_summary_strategic_vision": TemplateSection(
                id="executive_summary_strategic_vision",
                title="Executive Summary & Strategic Vision",
                content_focus="Business strategy, value propositions, high-level goals",
                keywords=["strategy", "vision", "mission", "goals", "objectives", "value", "proposition", "executive"],
                triggers=["strategic objectives", "business alignment", "value proposition", "mission statement"],
                content_types=["strategic_objectives", "value_propositions", "success_metrics"],
                priority=2
            ),
            "business_context_market_analysis": TemplateSection(
                id="business_context_market_analysis",
                title="Business Context & Market Analysis",
                content_focus="Market research, competitive landscape, business case",
                keywords=["market", "competitive", "business", "revenue", "analysis", "competition", "landscape"],
                triggers=["market segmentation", "competitive analysis", "business case", "revenue strategy"],
                content_types=["market_research", "competitive_analysis", "business_case", "risk_assessment"],
                priority=3
            ),
            "user_research_experience_design": TemplateSection(
                id="user_research_experience_design",
                title="User Research & Experience Design",
                content_focus="Personas, user journeys, accessibility requirements",
                keywords=["user", "persona", "journey", "experience", "accessibility", "design", "UX", "UI"],
                triggers=["user personas", "user journey", "accessibility standards", "user research"],
                content_types=["user_personas", "user_journeys", "accessibility_requirements", "ux_design"],
                priority=4
            ),
            "functional_requirements_features": TemplateSection(
                id="functional_requirements_features",
                title="Functional Requirements & Feature Specifications",
                content_focus="Feature definitions, user stories, acceptance criteria",
                keywords=["functional", "requirements", "features", "user stories", "acceptance", "criteria", "specifications"],
                triggers=["core features", "user stories", "acceptance criteria", "business rules"],
                content_types=["functional_requirements", "user_stories", "acceptance_criteria", "feature_specs"],
                priority=5
            ),
            "non_functional_requirements": TemplateSection(
                id="non_functional_requirements",
                title="Non-Functional Requirements (NFRs)",
                content_focus="Performance, security, compliance, scalability requirements",
                keywords=["performance", "security", "scalability", "compliance", "availability", "maintainability"],
                triggers=["performance requirements", "security requirements", "compliance standards", "scalability"],
                content_types=["performance_specs", "security_requirements", "compliance_standards", "scalability_requirements"],
                priority=6
            ),
            "aiml_integration_capabilities": TemplateSection(
                id="aiml_integration_capabilities",
                title="AI/ML Integration & Advanced Capabilities",
                content_focus="AI enablement, automation, self-improvement mechanisms",
                keywords=["AI", "ML", "machine learning", "artificial intelligence", "automation", "algorithm"],
                triggers=["AI integration", "ML models", "automation", "self-improvement"],
                content_types=["ai_requirements", "ml_integration", "automation_specs", "intelligent_features"],
                priority=7
            ),
            "technical_architecture_implementation": TemplateSection(
                id="technical_architecture_implementation",
                title="Technical Architecture & Implementation",
                content_focus="System architecture, technology decisions, deployment strategy",
                keywords=["architecture", "technical", "technology", "implementation", "deployment", "infrastructure"],
                triggers=["system architecture", "technology stack", "deployment strategy", "integration points"],
                content_types=["architecture_specs", "technology_decisions", "deployment_requirements", "integration_specs"],
                priority=8
            ),
            "success_metrics_performance": TemplateSection(
                id="success_metrics_performance",
                title="Success Metrics & Performance Measurement",
                content_focus="KPIs, measurement frameworks, analytics strategy",
                keywords=["metrics", "KPI", "measurement", "analytics", "performance", "success"],
                triggers=["success metrics", "KPIs", "measurement framework", "analytics"],
                content_types=["business_metrics", "product_kpis", "performance_metrics", "analytics_requirements"],
                priority=9
            ),
            "development_methodology_planning": TemplateSection(
                id="development_methodology_planning",
                title="Development Methodology & Project Planning",
                content_focus="Agile implementation, resource planning, timeline management",
                keywords=["development", "methodology", "agile", "planning", "project", "timeline", "resources"],
                triggers=["development methodology", "project planning", "agile", "resource planning"],
                content_types=["methodology_specs", "project_plans", "resource_requirements", "timeline_specifications"],
                priority=10
            ),
            "quality_assurance_testing": TemplateSection(
                id="quality_assurance_testing",
                title="Quality Assurance & Testing Strategy",
                content_focus="Testing frameworks, quality gates, acceptance criteria",
                keywords=["quality", "testing", "QA", "test", "validation", "verification"],
                triggers=["testing strategy", "quality gates", "test plans", "validation criteria"],
                content_types=["testing_requirements", "quality_standards", "test_strategies", "validation_criteria"],
                priority=11
            ),
            "launch_strategy_gtm": TemplateSection(
                id="launch_strategy_gtm",
                title="Launch Strategy & Go-to-Market",
                content_focus="Launch planning, market entry, post-launch operations",
                keywords=["launch", "go-to-market", "GTM", "rollout", "deployment", "market entry"],
                triggers=["launch strategy", "go-to-market", "rollout plan", "market entry"],
                content_types=["launch_plans", "gtm_strategy", "rollout_specifications", "market_entry_plans"],
                priority=12
            ),
            "governance_compliance_risk": TemplateSection(
                id="governance_compliance_risk",
                title="Governance, Compliance & Risk Management",
                content_focus="Regulatory compliance, risk mitigation, governance frameworks",
                keywords=["governance", "compliance", "risk", "regulatory", "mitigation", "framework"],
                triggers=["regulatory compliance", "risk management", "governance", "compliance framework"],
                content_types=["compliance_requirements", "risk_assessments", "governance_frameworks", "regulatory_specs"],
                priority=13
            ),
            "dependencies_assumptions_constraints": TemplateSection(
                id="dependencies_assumptions_constraints",
                title="Dependencies, Assumptions & Constraints",
                content_focus="Critical success factors, blockers, external dependencies",
                keywords=["dependencies", "assumptions", "constraints", "blockers", "external", "limitations"],
                triggers=["dependencies", "assumptions", "constraints", "external dependencies"],
                content_types=["dependency_specs", "assumption_documentation", "constraint_definitions", "external_dependencies"],
                priority=14
            ),
            "supporting_documentation_appendices": TemplateSection(
                id="supporting_documentation_appendices",
                title="Supporting Documentation & Appendices",
                content_focus="Reference materials, detailed artifacts, supplementary data",
                keywords=["documentation", "appendix", "reference", "supplementary", "artifacts", "supporting"],
                triggers=["reference materials", "supporting documentation", "appendices", "detailed artifacts"],
                content_types=["reference_materials", "supplementary_documentation", "detailed_artifacts", "appendices"],
                priority=15
            )
        }
        
        self.sections = sections_data
    
    def _initialize_classification_system(self):
        """Initialize the classification system with weighted scoring"""
        # Compile regex patterns for better performance
        for section in self.sections.values():
            section.keyword_patterns = [re.compile(r'\b' + re.escape(kw) + r'\b', re.IGNORECASE) 
                                      for kw in section.keywords]
            section.trigger_patterns = [re.compile(r'\b' + re.escape(trigger) + r'\b', re.IGNORECASE) 
                                      for trigger in section.triggers]
    
    def classify_content(self, content: str, source_file: str = "") -> Tuple[Optional[ClassificationResult], bool]:
        """
        Classify content to the most appropriate template section
        
        Returns:
            Tuple of (ClassificationResult or None, is_categorized)
        """
        best_match = None
        best_score = 0.0
        section_scores = {}
        
        # Clean and prepare content for analysis
        content_lower = content.lower()
        content_words = set(re.findall(r'\b\w+\b', content_lower))
        
        for section_id, section in self.sections.items():
            score = self._calculate_section_score(content, content_lower, content_words, section)
            section_scores[section_id] = score
            
            if score > best_score:
                best_score = score
                best_match = section
        
        # Determine if content is categorizable
        threshold = 0.3  # Minimum confidence threshold
        
        if best_score >= threshold and best_match:
            matched_keywords = self._get_matched_keywords(content, best_match)
            reasoning = self._generate_classification_reasoning(best_match, best_score, matched_keywords)
            
            result = ClassificationResult(
                section_id=best_match.id,
                confidence=best_score,
                matched_keywords=matched_keywords,
                reasoning=reasoning,
                content_snippet=content[:200] + "..." if len(content) > 200 else content
            )
            return result, True
        else:
            # Content couldn't be categorized with sufficient confidence
            self._add_uncategorized_content(content, source_file, section_scores)
            return None, False
    
    def _calculate_section_score(self, content: str, content_lower: str, content_words: set, section: TemplateSection) -> float:
        """Calculate matching score for a section"""
        score = 0.0
        
        # Keyword matching (weighted by frequency)
        keyword_matches = 0
        for pattern in section.keyword_patterns:
            matches = len(pattern.findall(content))
            keyword_matches += matches
        
        # Trigger phrase matching (higher weight)
        trigger_matches = 0
        for pattern in section.trigger_patterns:
            if pattern.search(content):
                trigger_matches += 1
        
        # Content type indicators
        content_type_matches = 0
        for content_type in section.content_types:
            if content_type.replace('_', ' ') in content_lower:
                content_type_matches += 1
        
        # Calculate weighted score
        score = (
            (keyword_matches * 0.3) +  # Keyword weight
            (trigger_matches * 0.5) +  # Trigger phrase weight
            (content_type_matches * 0.2)  # Content type weight
        )
        
        # Normalize score based on content length
        content_length_factor = min(1.0, len(content.split()) / 50)  # Normalize for 50+ words
        score *= content_length_factor
        
        # Apply section priority boost for better matches
        if score > 0:
            priority_boost = 1.0 + (1.0 / section.priority) * 0.1
            score *= priority_boost
        
        return min(score, 1.0)  # Cap at 1.0
    
    def _get_matched_keywords(self, content: str, section: TemplateSection) -> List[str]:
        """Get list of keywords that matched in the content"""
        matched = []
        for i, pattern in enumerate(section.keyword_patterns):
            if pattern.search(content):
                matched.append(section.keywords[i])
        
        for i, pattern in enumerate(section.trigger_patterns):
            if pattern.search(content):
                matched.append(section.triggers[i])
        
        return matched
    
    def _generate_classification_reasoning(self, section: TemplateSection, score: float, keywords: List[str]) -> str:
        """Generate human-readable reasoning for classification"""
        return f"Classified to '{section.title}' (confidence: {score:.2f}) based on matched terms: {', '.join(keywords[:5])}. Content aligns with section focus: {section.content_focus}"
    
    def _add_uncategorized_content(self, content: str, source_file: str, section_scores: Dict[str, float]):
        """Add content to uncategorized list with suggestions"""
        attempted_sections = [sid for sid, score in sorted(section_scores.items(), key=lambda x: x[1], reverse=True)[:3]]
        
        suggestions = []
        if section_scores:
            top_section = max(section_scores.items(), key=lambda x: x[1])
            if top_section[1] > 0.1:  # If there's some relevance
                suggestions.append(f"Consider '{self.sections[top_section[0]].title}' (partial match)")
        
        suggestions.append("Add to 'Supporting Documentation & Appendices' if reference material")
        suggestions.append("Flag for human review if critical business content")
        
        uncategorized = UncategorizedContent(
            content=content,
            source_file=source_file,
            attempted_sections=attempted_sections,
            reasoning=f"No section achieved minimum confidence threshold (0.3). Highest score: {max(section_scores.values()):.2f}",
            suggestions=suggestions
        )
        
        self.uncategorized_content.append(uncategorized)
    
    def batch_classify_content(self, content_items: List[Tuple[str, str]]) -> Dict[str, List[ClassificationResult]]:
        """
        Classify multiple content items and group by section
        
        Args:
            content_items: List of (content, source_file) tuples
            
        Returns:
            Dictionary mapping section_id to list of ClassificationResults
        """
        classified_by_section = {}
        
        for content, source_file in content_items:
            result, is_categorized = self.classify_content(content, source_file)
            
            if is_categorized and result:
                section_id = result.section_id
                if section_id not in classified_by_section:
                    classified_by_section[section_id] = []
                classified_by_section[section_id].append(result)
        
        return classified_by_section
    
    def get_uncategorized_content(self) -> List[UncategorizedContent]:
        """Get all content that couldn't be categorized"""
        return self.uncategorized_content
    
    def generate_classification_report(self) -> Dict:
        """Generate comprehensive classification report"""
        total_content = len(self.uncategorized_content)
        
        # Count classified content by section
        section_counts = {}
        for section_id, section in self.sections.items():
            section_counts[section_id] = {
                'title': section.title,
                'content_focus': section.content_focus,
                'classified_items': 0  # Would be updated during actual processing
            }
        
        report = {
            'template_file': str(self.template_path),
            'total_sections': len(self.sections),
            'section_details': section_counts,
            'uncategorized_count': len(self.uncategorized_content),
            'uncategorized_items': [
                {
                    'content_snippet': item.content[:100] + "..." if len(item.content) > 100 else item.content,
                    'source_file': item.source_file,
                    'suggestions': item.suggestions,
                    'reasoning': item.reasoning
                }
                for item in self.uncategorized_content
            ],
            'classification_accuracy': 0.0  # Would be calculated during processing
        }
        
        return report
    
    def export_classification_system(self) -> Dict:
        """Export classification system configuration for reuse"""
        return {
            'template_path': str(self.template_path),
            'sections': {
                section_id: {
                    'title': section.title,
                    'content_focus': section.content_focus,
                    'keywords': section.keywords,
                    'triggers': section.triggers,
                    'content_types': section.content_types,
                    'priority': section.priority
                }
                for section_id, section in self.sections.items()
            }
        }


def main():
    """CLI interface for testing the classification system"""
    import argparse
    
    parser = argparse.ArgumentParser(description="PRD Template Classification System")
    parser.add_argument("--template", required=True, help="Path to PRD template file")
    parser.add_argument("--test-content", help="Test content to classify")
    parser.add_argument("--export-config", help="Export classification configuration to file")
    
    args = parser.parse_args()
    
    try:
        classifier = PRDTemplateClassificationSystem(args.template)
        
        if args.test_content:
            result, is_categorized = classifier.classify_content(args.test_content)
            if is_categorized:
                print(f"Classification Result:")
                print(f"  Section: {result.section_id}")
                print(f"  Confidence: {result.confidence:.2f}")
                print(f"  Reasoning: {result.reasoning}")
            else:
                print("Content could not be categorized with sufficient confidence")
                uncategorized = classifier.get_uncategorized_content()
                if uncategorized:
                    print(f"Suggestions: {uncategorized[-1].suggestions}")
        
        if args.export_config:
            config = classifier.export_classification_system()
            with open(args.export_config, 'w') as f:
                yaml.dump(config, f, default_flow_style=False)
            print(f"Configuration exported to {args.export_config}")
            
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())