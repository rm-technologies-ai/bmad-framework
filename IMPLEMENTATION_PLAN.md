# PDF Document Ingestion Pipeline - Implementation Plan

## Overview
This document outlines the implementation of a standardized PDF document ingestion pipeline for the BMAD method, enforcing MD-only ingestion across all agents and workflows.

## Core Requirements Summary
- **Rule**: All PDFs must be converted to Markdown before BMAD agent ingestion
- **Converter**: Use existing Python script at `utilities/pdf-to-md-converter`
- **Structure**: Source PDFs in `input-documents/`, converted MDs in `input-documents-converted-to-md/`
- **Versioning**: Numerical suffixes for duplicate conversions (`document_v2.md`, etc.)
- **Priority**: Agents always reference highest numbered version

## Current State Analysis

### .bmad-core Structure
```
.bmad-core/
├── agents/           # 10 agent definition files
├── checklists/       # Quality control checklists  
├── data/            # Knowledge base and preferences
├── tasks/           # 17 task workflow definitions
├── templates/       # Document templates
├── utils/           # Utility scripts and helpers
├── workflows/       # Development workflow definitions
├── core-config.yaml # Core configuration
└── user-guide.md    # User documentation
```

### .claude Structure  
```
.claude/
├── commands/BMad/
│   ├── agents/      # 10 Claude command agents
│   └── tasks/       # 17 Claude command tasks
└── settings.local.json
```

## Implementation Phases

### Phase 1: Documentation and Planning ✅
- [x] Create `IMPLEMENTATION_PLAN.md` (this document)
- [x] Document current state analysis
- [x] Define integration points and dependencies

### Phase 2: Infrastructure Setup
1. **Create Folder Structure**
   ```
   input-documents/                    # Source PDFs (preserve hierarchy)
   input-documents-converted-to-md/    # Converted MDs (mirror hierarchy)
   utilities/                          # Conversion scripts
   ├── pdf-to-md-converter/           # Existing Python converter
   ├── pdf-ingestion-pipeline/        # New pipeline scripts
   └── validation-scripts/            # Quality validation
   ```

2. **Create Utility Scripts**
   - `utilities/pdf-ingestion-pipeline/convert-pdf.py` - Wrapper for conversion
   - `utilities/pdf-ingestion-pipeline/version-manager.py` - Version numbering logic
   - `utilities/pdf-ingestion-pipeline/validate-conversion.py` - Quality validation
   - `utilities/pdf-ingestion-pipeline/batch-converter.sh` - Batch processing

### Phase 3: Core Configuration Updates
1. **Update `.bmad-core/core-config.yaml`**
   ```yaml
   documentIngestion:
     pdfConversionRequired: true
     sourceDocumentsPath: input-documents
     convertedDocumentsPath: input-documents-converted-to-md
     conversionScript: utilities/pdf-to-md-converter
     versioningEnabled: true
     latestVersionPriority: true
   
   devLoadAlwaysFiles:
     - docs/architecture/coding-standards.md
     - docs/architecture/tech-stack.md  
     - docs/architecture/source-tree.md
     - docs/pdf-ingestion-rules.md
   ```

2. **Create `.bmad-core/data/pdf-ingestion-rules.md`**
   - Document ingestion policies
   - Conversion validation requirements
   - Version management rules

3. **Update `.bmad-core/workflows/`**
   - Add `document-ingestion-workflow.md`
   - Update existing workflows to include PDF check steps

### Phase 4: Agent Definition Updates
Update all 10 agents in `.bmad-core/agents/` with:
1. **PDF Conversion Rules**
   ```yaml
   documentIngestionRules:
     - NEVER ingest PDF files directly
     - ALWAYS check for existing MD conversion first
     - USE highest version number when multiple conversions exist
     - TRIGGER conversion process if MD version missing
     - VALIDATE conversion quality before use
   ```

2. **Pre-processing Steps**
   - Add PDF detection to agent activation
   - Include conversion validation in workflows
   - Update error handling for conversion failures

### Phase 5: Claude Integration Updates
1. **Update `.claude/commands/BMad/agents/`**
   - Mirror PDF ingestion rules from .bmad-core agents
   - Add Claude-specific conversion commands
   - Update help text with PDF procedures

2. **Create `.claude/workflows/`**
   - `pdf-conversion-workflow.md` - Claude-specific instructions
   - Integration with existing Claude workflows

### Phase 6: Documentation Updates
1. **Update `CLAUDE.md`**
   - Add "PDF Document Ingestion" section
   - Include conversion workflow examples
   - Document folder structure and usage

2. **Create `PDF_CONVERSION_WORKFLOW.md`**
   - User-facing conversion instructions
   - Troubleshooting guide
   - Quality validation procedures

## Technical Implementation Details

### Conversion Pipeline Flow
```
1. User places PDF in input-documents/
2. Agent detects PDF reference request
3. Check input-documents-converted-to-md/ for existing conversion
4. If exists: Use latest version (highest _v{n} suffix)
5. If missing: Trigger conversion process
6. Validate conversion quality
7. Agent proceeds with MD file ingestion
```

### Version Management Logic
```python
def get_next_version(base_filename, converted_path):
    existing_versions = glob(f"{converted_path}/{base_filename}_v*.md")
    if not existing_versions:
        return f"{base_filename}.md"
    
    version_numbers = [extract_version_number(f) for f in existing_versions]
    next_version = max(version_numbers) + 1
    return f"{base_filename}_v{next_version}.md"
```

### Error Handling Strategy
- **Conversion Failures**: Log error, notify user, halt agent processing
- **Version Conflicts**: Auto-increment to next available version
- **Missing Source**: Error with specific file path guidance
- **Quality Validation Failures**: Retry conversion with different parameters

## Integration Points

### Agent Startup Sequences
All agents must:
1. Load PDF ingestion rules from `docs/pdf-ingestion-rules.md`
2. Validate any document references against conversion requirements
3. Pre-process any PDF references before main workflow execution

### Workflow Integration
Update existing workflows:
- **Planning workflows**: Add PDF conversion validation steps
- **Development workflows**: Include conversion checks in story processing  
- **Review workflows**: Validate document sources and versions

### Configuration Dependencies
- `core-config.yaml` - Central configuration
- `pdf-ingestion-rules.md` - Policy definitions
- `technical-preferences.md` - Conversion preferences

## Testing Strategy

### Unit Tests
- Version numbering logic
- File path hierarchy preservation  
- Conversion quality validation
- Error handling scenarios

### Integration Tests
- End-to-end PDF to agent ingestion
- Multi-version document handling
- Agent rule enforcement
- Claude integration functionality

### Validation Requirements
1. **Conversion Quality**: Text extraction accuracy, formatting preservation
2. **Version Management**: Correct numbering, latest version priority
3. **Agent Compliance**: PDF rejection, MD preference validation
4. **Error Handling**: Graceful failure modes, user notifications

## Risk Mitigation

### Technical Risks
- **Conversion Quality Issues**: Implement quality scoring and manual review flags
- **Version Management Conflicts**: Atomic file operations, lock mechanisms
- **Performance Impact**: Batch processing options, caching strategies

### Process Risks  
- **User Adoption**: Clear documentation, error messages, training materials
- **Agent Compliance**: Comprehensive rule enforcement, validation checks
- **Workflow Disruption**: Gradual rollout, fallback mechanisms

## Success Criteria
- [ ] All agents enforce PDF conversion requirement
- [ ] Version management works correctly
- [ ] Folder hierarchy preserved during conversion
- [ ] Claude integration functional
- [ ] Documentation complete and accurate
- [ ] Validation tests pass
- [ ] Error handling robust

## Deliverables Checklist
- [ ] Updated `.bmad-core/` configuration files
- [ ] Updated `.claude/` configuration files  
- [ ] `IMPLEMENTATION_PLAN.md` (this document)
- [ ] `PDF_CONVERSION_WORKFLOW.md` user guide
- [ ] Updated `CLAUDE.md` with new procedures
- [ ] Utility scripts and validation tools
- [ ] Test results and examples

## Next Steps
1. Create folder structure and utility scripts
2. Update core configuration files
3. Modify all agent definitions
4. Update Claude integration
5. Create user documentation
6. Implement validation and testing
7. Deploy and validate end-to-end pipeline