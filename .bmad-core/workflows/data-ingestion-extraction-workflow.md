# BMAD Data Ingestion Extraction Plan Workflow

## Overview
This workflow implements a two-phase extraction process that ensures data integrity through user-approved plans for all BMAD agents that read and shard project data.

## Core Principles
- **NEVER delete existing information** without explicit user approval
- **DEFAULT to aggregation/addition operations** only
- **Generate detailed, verbatim extraction plans** for user review
- **Execute only approved operations**

## Workflow Architecture

### Phase 1: Extraction Plan Generation

When agents encounter source documents, they must:

1. **Analyze Source Document**
   - Identify document type and content structure
   - Catalog key data elements for extraction
   - Determine target locations in project structure

2. **Generate Extraction Plan**
   - Create `{document-name}-extraction-plan.md` file
   - Classify operations as SAFE or REQUIRES_APPROVAL
   - Provide verbatim content examples
   - Include risk assessments for modifications

3. **Present Plan to User**
   - Display extraction plan summary
   - Request approval for risky operations
   - Provide execution time estimates

### Phase 2: Extraction Execution

After user approval:

1. **Validate Plan File**
   - Parse extraction plan markdown
   - Verify all target paths exist
   - Confirm approval status

2. **Create Backups**
   - Backup all files to be modified
   - Generate timestamp-based backup directory
   - Create rollback commands

3. **Execute Operations**
   - Perform safe operations automatically
   - Execute only approved risky operations
   - Log all changes with timestamps

4. **Generate Reports**
   - Create detailed execution log
   - Generate diff reports for changes
   - Provide file checksums for verification

## Extraction Plan Template

### Standard Plan Structure
```markdown
# {Document Name} Extraction Plan

## Source Document Analysis
- **Document Type**: [document type]
- **Content Summary**: [2-3 sentence overview]
- **Key Data Elements Identified**: 
  - [element 1]
  - [element 2]
  - [element 3]

## Proposed Extractions

### SAFE OPERATIONS (Auto-Approved)
#### Information Aggregations
1. **Target Location**: [specific file/section path]
   **Operation**: ADD
   **Content to Add**:
   ```
   [exact text to be inserted]
   ```
   **Rationale**: [why this addition improves the dataset]
   **Dependencies**: [any prerequisites]

### REQUIRES USER APPROVAL
#### Information Modifications
1. **Target Location**: [specific file/section path]
   **Operation**: [DELETE/MODIFY/DEDUPLICATE/RESTRUCTURE]
   **Current Content**:
   ```
   [existing text that would be affected]
   ```
   **Proposed Content**:
   ```
   [new text or DELETED if removal]
   ```
   **Rationale**: [detailed justification]
   **Risk Assessment**: [potential data loss or impact]
   **Approval Status**: PENDING

## Execution Summary
- **Safe Operations**: [count] additions/aggregations
- **Approval Required**: [count] modifications/deletions
- **Estimated Completion Time**: [time estimate]

## Execution Commands
```bash
# Commands to execute this plan (generated automatically)
[Detailed step-by-step file operations]
```
```

### Operation Classifications

#### SAFE OPERATIONS (Auto-Approved)
- **ADD**: Append new information to existing files
- **AGGREGATE**: Combine related information sections
- **CREATE**: Generate new files with extracted content
- **INDEX**: Create cross-reference or navigation structures

#### REQUIRES USER APPROVAL
- **DELETE**: Remove existing content
- **MODIFY**: Change existing text content
- **RESTRUCTURE**: Reorganize file or section structure
- **DEDUPLICATE**: Remove duplicate information
- **MERGE**: Combine conflicting information sources

### Risk Assessment Levels

#### LOW RISK
- Adding new information to empty sections
- Creating new files in designated directories
- Appending to existing lists or indexes

#### MEDIUM RISK  
- Modifying existing content structure
- Reorganizing section headings
- Deduplicating similar content

#### HIGH RISK
- Deleting existing information
- Overwriting user-created content
- Restructuring core project files

## Integration with BMAD Agents

### Agent Responsibilities

All data ingestion agents must:

1. **Pre-Processing Check**
   ```yaml
   before_data_ingestion:
     - detect_source_documents()
     - load_prd_template_structure()
     - validate_template_classification_system()
     - check_for_existing_extraction_plans()
     - validate_target_directory_structure()
   ```

2. **Template-Based Classification**
   ```yaml
   template_classification:
     - load_template_section_mappings()
     - classify_content_to_template_sections()
     - identify_uncategorizable_content()
     - generate_classification_report()
     - flag_content_for_human_review()
   ```

3. **Extraction Plan Generation**
   ```yaml
   plan_generation:
     - analyze_source_content()
     - identify_extraction_targets()
     - classify_operations_by_risk()
     - map_content_to_template_sections()
     - generate_plan_markdown()
     - request_user_approval()
   ```

4. **Plan Execution**
   ```yaml
   plan_execution:
     - validate_plan_file()
     - create_file_backups()
     - execute_safe_operations()
     - execute_approved_operations()
     - populate_template_sections()
     - generate_versioned_output()
     - generate_execution_log()
   ```

### Agent-Specific Integration

#### PM Agent Integration
```yaml
prd_extraction_workflow:
  template_file: templates/PRD-template.md
  template_mode: enforced_structure
  source_types: [requirements_docs, stakeholder_interviews, market_research]
  target_files: [docs/prd-v{n}.md, .ai/prd-generation/]
  classification_sections:
    - document_foundation_context
    - executive_summary_strategic_vision
    - business_context_market_analysis
    - user_research_experience_design
    - functional_requirements_features
    - non_functional_requirements
    - aiml_integration_capabilities
    - technical_architecture_implementation
    - success_metrics_performance
    - development_methodology_planning
    - quality_assurance_testing
    - launch_strategy_gtm
    - governance_compliance_risk
    - dependencies_assumptions_constraints
    - supporting_documentation_appendices
  safe_operations: [template_section_population, content_classification]
  approval_required: [uncategorized_content_placement, template_structure_deviation]
  error_handling:
    uncategorizable_content: flag_for_human_review
    template_violations: halt_and_report
    version_conflicts: create_new_version
```

#### Architect Agent Integration  
```yaml
architecture_extraction_workflow:
  source_types: [technical_specs, system_diagrams, api_docs]
  target_files: [docs/architecture.md, docs/architecture/]
  safe_operations: [add_components, aggregate_patterns]
  approval_required: [modify_existing_architecture, restructure_diagrams]
```

#### Dev Agent Integration
```yaml
development_extraction_workflow:
  source_types: [code_documentation, technical_guides, api_references]
  target_files: [docs/architecture/coding-standards.md, docs/development/]
  safe_operations: [add_standards, aggregate_examples]
  approval_required: [modify_existing_standards, restructure_guidelines]
```

## Command Integration

### New Agent Commands

#### Generate Extraction Plan
```bash
Command: generate-extraction-plan {source-document-path}
Purpose: Analyze document and create extraction plan
Output: {document-name}-extraction-plan.md
```

#### Execute Extraction Plan
```bash
Command: execute-extraction-plan {plan-file-path}
Purpose: Execute approved operations from plan
Output: Execution log and modified files
```

#### Review Extraction Plan
```bash
Command: review-extraction-plan {plan-file-path}  
Purpose: Display plan summary and approval status
Output: Plan overview with operation counts
```

#### Approve Operation
```bash
Command: approve-operation {plan-file-path} {operation-number}
Purpose: Mark specific operation as approved
Output: Updated plan file with approval status
```

## File Structure Integration

### Generated Files Location
```
.ai/extraction-plans/
├── {document-name}-extraction-plan.md
├── {document-name}-backup-{timestamp}/
├── {document-name}-execution-log.md
└── approved-plans/
    └── {document-name}-approved-plan.md
```

### Backup Structure
```
.ai/backups/{timestamp}/
├── docs/
├── .bmad-core/
└── extraction-rollback-commands.sh
```

## Quality Assurance Protocol

### Pre-Execution Validation
- **Plan File Syntax**: Validate markdown formatting
- **Target Path Verification**: Confirm all paths exist
- **Operation Dependencies**: Check prerequisite operations
- **Approval Status**: Verify required approvals obtained

### Execution Monitoring
- **File Lock Management**: Prevent concurrent modifications
- **Progress Tracking**: Log operation completion status
- **Error Handling**: Graceful failure recovery
- **Rollback Preparation**: Generate undo commands

### Post-Execution Verification
- **File Integrity**: Validate modified file checksums
- **Content Verification**: Confirm intended changes applied
- **Backup Validation**: Verify backup completeness
- **Log Generation**: Create detailed execution report

## Error Handling Strategies

### Common Error Scenarios

#### Missing Target Files
```yaml
error_handling:
  missing_target:
    action: create_parent_directories
    log: "Created missing directory structure"
    continue: true
```

#### Permission Errors
```yaml
error_handling:
  permission_denied:
    action: log_error_and_skip
    log: "Permission denied, operation skipped"
    continue: true
```

#### Content Conflicts
```yaml
error_handling:
  content_conflict:
    action: flag_for_user_review
    log: "Content conflict detected, user approval required"
    continue: false
```

### Recovery Mechanisms

#### Automatic Recovery
- Skip failed operations and continue
- Log all errors with timestamps
- Generate partial execution reports
- Preserve backup integrity

#### Manual Recovery
- Provide rollback commands
- Generate conflict resolution suggestions
- Create manual merge instructions
- Offer re-execution options

## Performance Optimization

### Batch Processing
- Group similar operations together
- Minimize file I/O operations
- Cache file content during execution
- Parallelize independent operations

### Memory Management
- Stream large file operations
- Release resources after use
- Monitor memory usage during execution
- Implement progress checkpoints

### Cross-Platform Compatibility
- Use forward slashes in all paths
- Handle different line endings gracefully
- Support Unicode content properly
- Test on multiple operating systems

## Monitoring and Reporting

### Metrics Collection
- **Operation Success Rate**: Track successful vs failed operations
- **Execution Time**: Monitor performance across different document types
- **User Approval Rate**: Track approval patterns for risk assessment
- **Backup Utilization**: Monitor backup storage usage

### Report Generation
- **Daily Extraction Summary**: Operations performed per day
- **Agent Performance Report**: Extraction efficiency by agent
- **Risk Assessment Report**: Analysis of operation risk levels
- **User Approval Patterns**: Insights into approval decision trends

This workflow ensures that all BMAD data ingestion operations are transparent, reversible, and user-controlled, maintaining data integrity throughout the development process.