# Create Template-Based PRD

## ⚠️ CRITICAL EXECUTION NOTICE ⚠️

**THIS IS AN EXECUTABLE WORKFLOW - NOT REFERENCE MATERIAL**

This task enforces the MANDATORY use of templates/PRD-template.md for ALL PRD generation.

**CRITICAL TEMPLATE RULES:**
1. **MANDATORY template usage** - ALL PRDs MUST use `/templates/PRD-template.md` structure
2. **NO dynamic sections** - NEVER create new sections or modify template structure  
3. **Classification-based processing** - ALL content MUST be classified to predefined template sections
4. **Version control** - Generate versioned files (prd-v1.md, prd-v2.md), keep template read-only
5. **Error handling** - Flag uncategorizable content for human review, NEVER force into wrong sections

## Phase 1: Template Validation & Initialization

### Step 1: Validate Template File
```bash
# Verify template exists and is readable
python3 utilities/prd-template-processor/template_validator.py --template templates/PRD-template.md --validate-structure
```

### Step 2: Initialize Classification System
Load the template-based classification system:
- Parse 15 predefined sections from PRD-template.md
- Initialize content classification triggers and keywords
- Set confidence threshold (minimum 0.3 for automatic placement)
- Create uncategorized content handling system

### Step 3: Source Document Preparation
**CRITICAL PDF INGESTION RULES:**
- NEVER ingest PDF files directly
- Check for existing conversions in `input-documents-converted-to-md/`
- Use highest version number (e.g., `document_v3.md` over `document.md`)
- Trigger conversion if no MD version exists
- Validate conversion quality before use

## Phase 2: Content Ingestion & Classification

### Step 4: Analyze Source Documents
For each source document:
1. **Read converted MD files** (never PDFs directly)
2. **Extract content sections** preserving source attribution
3. **Identify content types** (requirements, architecture, business case, etc.)
4. **Create content inventory** with source file references

### Step 5: Template-Based Content Classification
```python
# Use classification system to map content to template sections
from utilities.prd_template_processor.classification_system import PRDTemplateClassificationSystem

classifier = PRDTemplateClassificationSystem('templates/PRD-template.md')
classified_content = {}
uncategorized_content = []

for content_item in extracted_content:
    result, is_categorized = classifier.classify_content(content_item.text, content_item.source)
    
    if is_categorized:
        section_id = result.section_id
        if section_id not in classified_content:
            classified_content[section_id] = []
        classified_content[section_id].append(result)
    else:
        uncategorized_content.append(content_item)
```

### Step 6: Handle Uncategorizable Content
For content that cannot be classified with ≥0.3 confidence:
1. **Flag for human review** - Add to `.ai/prd-generation/uncategorized-content-review.md`
2. **Document reasoning** - Explain why classification failed
3. **Provide suggestions** - Offer potential section placements or alternatives
4. **NEVER force placement** - Do not place content in inappropriate sections

## Phase 3: PRD Generation & Population

### Step 7: Load Template Structure
Read the complete template structure from `templates/PRD-template.md`:
- Preserve exact section headings and hierarchy
- Maintain content aggregation focus descriptions
- Keep all structural elements intact

### Step 8: Populate Template Sections
For each of the 15 predefined sections:

#### Section 1: DOCUMENT FOUNDATION & CONTEXT
- Populate with: Document control, definitions, compliance frameworks
- Source: Version control data, glossaries, standards references

#### Section 2: EXECUTIVE SUMMARY & STRATEGIC VISION
- Populate with: Business strategy, value propositions, high-level goals
- Source: Strategic objectives, mission statements, value propositions

#### Section 3: BUSINESS CONTEXT & MARKET ANALYSIS
- Populate with: Market research, competitive landscape, business case
- Source: Market analysis, competitive data, business justification

#### Section 4: USER RESEARCH & EXPERIENCE DESIGN
- Populate with: Personas, user journeys, accessibility requirements
- Source: User research, persona definitions, UX requirements

#### Section 5: FUNCTIONAL REQUIREMENTS & FEATURE SPECIFICATIONS
- Populate with: Feature definitions, user stories, acceptance criteria
- Source: Requirements documents, feature specifications, user stories

#### Section 6: NON-FUNCTIONAL REQUIREMENTS (NFRS)
- Populate with: Performance, security, compliance, scalability requirements
- Source: Technical requirements, security specs, performance criteria

#### Section 7: AI/ML INTEGRATION & ADVANCED CAPABILITIES
- Populate with: AI enablement, automation, self-improvement mechanisms
- Source: AI requirements, ML specifications, automation plans

#### Section 8: TECHNICAL ARCHITECTURE & IMPLEMENTATION
- Populate with: System architecture, technology decisions, deployment strategy
- Source: Architecture documents, technology decisions, deployment plans

#### Section 9: SUCCESS METRICS & PERFORMANCE MEASUREMENT
- Populate with: KPIs, measurement frameworks, analytics strategy
- Source: Business metrics, success criteria, measurement plans

#### Section 10: DEVELOPMENT METHODOLOGY & PROJECT PLANNING
- Populate with: Agile implementation, resource planning, timeline management
- Source: Project plans, methodology specs, resource requirements

#### Section 11: QUALITY ASSURANCE & TESTING STRATEGY
- Populate with: Testing frameworks, quality gates, acceptance criteria
- Source: Testing requirements, QA plans, quality standards

#### Section 12: LAUNCH STRATEGY & GO-TO-MARKET
- Populate with: Launch planning, market entry, post-launch operations
- Source: Launch plans, GTM strategy, rollout specifications

#### Section 13: GOVERNANCE, COMPLIANCE & RISK MANAGEMENT
- Populate with: Regulatory compliance, risk mitigation, governance frameworks
- Source: Compliance requirements, risk assessments, governance specs

#### Section 14: DEPENDENCIES, ASSUMPTIONS & CONSTRAINTS
- Populate with: Critical success factors, blockers, external dependencies
- Source: Dependency documentation, assumptions, constraint definitions

#### Section 15: SUPPORTING DOCUMENTATION & APPENDICES
- Populate with: Reference materials, detailed artifacts, supplementary data
- Source: Supporting documents, detailed specs, reference materials

### Step 9: Generate Versioned PRD File
```python
from utilities.prd_template_processor.version_manager import PRDVersionManager

# Initialize version manager
version_manager = PRDVersionManager('.', 'templates/PRD-template.md')

# Create versioned PRD
prd_content = populate_template_with_classified_content(classified_content)
source_documents = [doc.path for doc in processed_documents]

prd_file_path = version_manager.create_new_version(
    content=prd_content,
    source_documents=source_documents,
    classification_report_path='.ai/prd-generation/classification-report.md',
    created_by='bmad-pm-agent',
    status='draft'
)

print(f"Generated PRD version: {prd_file_path}")
```

## Phase 4: Validation & Quality Assurance

### Step 10: Validate Template Compliance
```bash
# Validate generated PRD against template structure
python3 utilities/prd-template-processor/template_validator.py \
    --template templates/PRD-template.md \
    --prd-file docs/prd-v{n}.md \
    --output-report .ai/prd-generation/validation-report.md
```

### Step 11: Generate Reports
Create comprehensive documentation:

#### Classification Report
- Content classification statistics
- Confidence scores by section
- Uncategorized content summary
- Source attribution mapping

#### Generation Log  
- Processing timeline and steps
- Source document inventory
- Version control metadata
- Quality assurance results

#### Validation Report
- Template compliance verification
- Structural integrity check
- Content completeness analysis
- Recommendations for improvement

## Phase 5: Finalization & Handoff

### Step 12: Review Uncategorized Content
Present flagged content to user for review:
1. **Display uncategorized items** with context and reasoning
2. **Provide placement suggestions** based on section analysis
3. **Allow manual classification** with user guidance
4. **Update PRD version** if manual placements approved

### Step 13: Final Validation & Approval
```bash
# Final comprehensive validation
python3 utilities/prd-template-processor/template_validator.py \
    --template templates/PRD-template.md \
    --prd-file docs/prd-v{n}.md \
    --json-output
```

### Step 14: Archive and Document
1. **Update version metadata** with final status
2. **Archive supporting files** in `.ai/prd-generation/prd-v{n}/`
3. **Create version summary** for project documentation
4. **Generate handoff documentation** for next phase agents

## Error Handling Protocols

### Template Validation Failures
```yaml
error: template_not_found
response: halt_processing
action: verify_template_path_and_permissions
```

### Classification System Failures
```yaml
error: classification_threshold_not_met
response: flag_for_human_review
action: add_to_uncategorized_content_queue
```

### Version Control Conflicts
```yaml
error: version_file_exists
response: increment_version_number
action: create_new_versioned_file
```

### Content Integration Failures
```yaml
error: section_population_failed
response: log_error_and_continue
action: mark_section_as_tbd_for_manual_completion
```

## Quality Gates

Before completion, verify:
- ✅ Template structure exactly preserved
- ✅ All 15 sections populated or marked TBD
- ✅ No unauthorized structural modifications
- ✅ Version control metadata complete
- ✅ Classification report generated
- ✅ Validation passes with score ≥ 0.8
- ✅ Uncategorized content properly flagged
- ✅ Source attribution documented

## Output Files

### Primary Output
- `docs/prd-v{n}.md` - Versioned PRD file with metadata header

### Supporting Files
- `.ai/prd-generation/classification-report.md` - Content classification details
- `.ai/prd-generation/uncategorized-content-review.md` - Flagged content
- `.ai/prd-generation/validation-report.md` - Template compliance report
- `.ai/prd-generation/prd-v{n}/generation-log.md` - Process documentation
- `.ai/prd-generation/version_metadata.json` - Version control data

## Success Criteria

Task completion requires:
1. **Template compliance** - PRD structure matches template exactly
2. **Content classification** - All content properly categorized or flagged
3. **Version control** - Proper versioning with metadata
4. **Quality validation** - Validation score ≥ 0.8
5. **Documentation** - Complete audit trail and reports
6. **Error handling** - All uncategorizable content flagged for review

**VIOLATION INDICATOR:** If PRD contains sections not in templates/PRD-template.md or modifies template structure, the task has failed its core requirements.