# Template-Based PRD Workflow

## Overview
This workflow enforces the use of the predefined PRD-template.md for all PRD generation, ensuring consistent structure and preventing dynamic section creation.

## Core Principles
- **MANDATORY template usage**: All PRDs must use `/templates/PRD-template.md` structure
- **Classification-based ingestion**: All input data must be classified according to template sections
- **No dynamic sections**: Never create new sections or modify template structure
- **Version-controlled output**: Generated PRDs are versioned files, template remains read-only
- **Error handling**: Uncategorizable content flagged for human review

## Workflow Architecture

### Phase 1: Template Validation & Initialization
1. **Load PRD Template**
   - Read `/templates/PRD-template.md` 
   - Parse section structure and classification focuses
   - Validate template integrity and section mapping

2. **Initialize Classification System**
   - Create section classification map from template
   - Load content aggregation focus areas for each section
   - Initialize error handling for uncategorizable content

### Phase 2: Content Ingestion & Classification
1. **Document Analysis**
   - Analyze source documents (PDFs converted to MD)
   - Extract raw content preserving source attribution
   - Identify content type and context

2. **Template-Based Classification**
   - Map content to PRD template sections using classification focuses
   - Apply section-specific content aggregation rules
   - Flag content that doesn't fit predefined sections

3. **Content Validation**
   - Verify all content has been classified
   - Generate flagged content report for human review
   - Validate classification accuracy

### Phase 3: PRD Population & Generation
1. **Template Population**
   - Use read-only template as structure foundation
   - Populate each section with classified content
   - Maintain template section order and hierarchy

2. **Version Control**
   - Generate versioned PRD file (e.g., `prd-v1.md`, `prd-v2.md`)
   - Never modify original template file
   - Track version history and changes

3. **Quality Assurance**
   - Validate all sections populated according to template
   - Verify no sections added/removed/modified from template
   - Generate completion report

## Section Classification System

Based on the PRD template structure, content is classified into these sections:

### 1. DOCUMENT FOUNDATION & CONTEXT
**Triggers**: Document control, definitions, compliance frameworks, glossaries
**Content Types**: Version control, change logs, terminology, standards references

### 2. EXECUTIVE SUMMARY & STRATEGIC VISION
**Triggers**: Business strategy, value propositions, high-level goals, mission statements
**Content Types**: Strategic objectives, success metrics frameworks

### 3. BUSINESS CONTEXT & MARKET ANALYSIS
**Triggers**: Market research, competitive analysis, business case, revenue strategy
**Content Types**: Market segmentation, competitive matrices, risk assessments

### 4. USER RESEARCH & EXPERIENCE DESIGN
**Triggers**: Personas, user journeys, accessibility requirements, user research
**Content Types**: User personas, journey mapping, accessibility standards

### 5. FUNCTIONAL REQUIREMENTS & FEATURE SPECIFICATIONS
**Triggers**: Feature definitions, user stories, acceptance criteria, business rules
**Content Types**: Core features, epics, data models, business logic

### 6. NON-FUNCTIONAL REQUIREMENTS (NFRS)
**Triggers**: Performance, security, compliance, scalability requirements
**Content Types**: Performance metrics, security frameworks, compliance standards

### 7. AI/ML INTEGRATION & ADVANCED CAPABILITIES
**Triggers**: AI enablement, automation, ML models, self-improvement
**Content Types**: ML integration points, automation opportunities, AI readiness

### 8. TECHNICAL ARCHITECTURE & IMPLEMENTATION
**Triggers**: System architecture, technology decisions, deployment strategy
**Content Types**: Architecture patterns, technology stack, integration points

### 9. SUCCESS METRICS & PERFORMANCE MEASUREMENT
**Triggers**: KPIs, measurement frameworks, analytics strategy
**Content Types**: Business metrics, product KPIs, user experience metrics

### 10. DEVELOPMENT METHODOLOGY & PROJECT PLANNING
**Triggers**: Agile implementation, resource planning, timeline management
**Content Types**: Development methodology, MVP definition, resource planning

### 11. QUALITY ASSURANCE & TESTING STRATEGY
**Triggers**: Testing frameworks, quality gates, acceptance criteria
**Content Types**: Testing strategy, quality gates, validation criteria

### 12. LAUNCH STRATEGY & GO-TO-MARKET
**Triggers**: Launch planning, market entry, post-launch operations
**Content Types**: Rollout strategy, GTM planning, training materials

### 13. GOVERNANCE, COMPLIANCE & RISK MANAGEMENT
**Triggers**: Regulatory compliance, risk mitigation, governance frameworks
**Content Types**: Compliance requirements, risk matrices, governance processes

### 14. DEPENDENCIES, ASSUMPTIONS & CONSTRAINTS
**Triggers**: Critical success factors, blockers, external dependencies
**Content Types**: Technical dependencies, business assumptions, constraints

### 15. SUPPORTING DOCUMENTATION & APPENDICES
**Triggers**: Reference materials, detailed artifacts, supplementary data
**Content Types**: Architecture diagrams, research findings, detailed documentation

## Error Handling System

### Uncategorizable Content Handling
When content cannot be classified into predefined template sections:

1. **Flag for Review**
   - Add to `uncategorized-content-review.md` file
   - Include source attribution and context
   - Provide classification attempt reasoning

2. **Review Process**
   - Present flagged content to human reviewer
   - Suggest potential reclassification approaches
   - Allow reviewer to approve placement or request template enhancement

3. **Resolution Options**
   - **Reclassify**: Map to existing section with human guidance
   - **Supplementary**: Add to Supporting Documentation section
   - **External**: Move to separate document outside PRD scope
   - **Template Enhancement**: Request template section addition (rare)

### Error Types and Responses

#### Content Overlap Conflicts
```yaml
error_type: content_overlap
response: flag_for_human_review
action: present_both_options_with_context
resolution: human_selects_primary_section
```

#### Missing Template Sections
```yaml
error_type: template_section_missing
response: halt_processing
action: validate_template_integrity
resolution: reload_template_or_abort
```

#### Version Control Conflicts
```yaml
error_type: version_conflict
response: create_new_version
action: increment_version_number
resolution: generate_versioned_file
```

## Integration Points

### PM Agent Integration
The PM agent workflow integrates with this system by:
- Loading template classification system during initialization
- Using template-based content aggregation during PRD creation
- Enforcing version control for PRD outputs

### Extraction Workflow Integration
The existing extraction workflow is enhanced to:
- Perform template-based classification during extraction planning
- Use template section focuses for content categorization
- Generate template-compliant extraction plans

### Quality Assurance Integration
QA processes validate:
- PRD structure matches template exactly
- All content properly classified and placed
- No unauthorized template modifications
- Version control integrity maintained

## Command Integration

### New Template-Based Commands

#### Generate Template-Based PRD
```bash
Command: generate-template-prd {source-documents}
Purpose: Generate PRD using predefined template structure
Output: Versioned PRD file with classification report
```

#### Validate PRD Against Template
```bash
Command: validate-prd-template {prd-file-path}
Purpose: Validate PRD structure matches template
Output: Compliance report with any violations
```

#### Review Uncategorized Content
```bash
Command: review-uncategorized-content
Purpose: Display content flagged for human review
Output: Categorized list of flagged content with context
```

#### Classify Content to Template
```bash
Command: classify-content {content-file} {template-section}
Purpose: Manually classify content to template section
Output: Updated classification with confirmation
```

## File Structure

### Generated Files Location
```
.ai/prd-generation/
├── prd-v{n}.md                    # Versioned PRD output
├── classification-report.md        # Content classification details
├── uncategorized-content-review.md # Flagged content for review
├── template-validation-report.md   # Template compliance report
└── generation-history/
    ├── prd-v{n}-generation-log.md
    └── prd-v{n}-source-attribution.md
```

### Template Files
```
templates/
└── PRD-template.md                 # READ-ONLY template structure
```

### Working Files
```
docs/
├── prd-v{current}.md              # Current working PRD version
└── prd-archive/
    └── prd-v{n}.md                # Archived PRD versions
```

## Validation Protocols

### Pre-Generation Validation
- Template file exists and is readable
- Template structure is parseable
- Classification system properly initialized
- Source documents converted from PDF to MD

### Generation Validation  
- All content classified to template sections
- No unauthorized template modifications
- Version numbering correct and sequential
- All flagged content properly documented

### Post-Generation Validation
- Output PRD structure exactly matches template
- All template sections present (populated or marked as TBD)
- Version control metadata accurate
- Classification report complete

## Performance Optimization

### Template Caching
- Cache parsed template structure for reuse
- Cache section classification mappings
- Minimize template file I/O operations

### Batch Classification
- Process multiple content pieces in classification batches
- Group similar content types for efficient processing
- Parallelize independent classification operations

### Memory Management
- Stream large document processing
- Release classification resources after use
- Monitor memory usage during template population

This template-based workflow ensures consistent, predictable PRD generation while maintaining flexibility for content classification and error handling.