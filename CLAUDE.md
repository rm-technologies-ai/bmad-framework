# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a BMad-Method framework repository template that serves as a foundation for agile AI-driven development projects. The BMad-Method (Breakthrough Method of Agile AI-driven Development) is a comprehensive agentic development methodology with specialized AI agents for planning, architecture, development, QA, and project management.

## BMad-Method Architecture

### Core Framework Structure
- `.bmad-core/` - Core BMad framework files (agents, templates, workflows)
- `.claude/commands/BMad/` - Claude Code integration with BMad agents and tasks
- `docs/` - Project documentation (PRD, architecture, stories)
- `.ai/` - AI workspace and debug logs
- `input-documents/` - Source PDF documents for conversion
- `input-documents-converted-to-md/` - Converted Markdown documents
- `utilities/` - Conversion scripts and validation tools

### Available Agent Commands
Execute these with `/` prefix in Claude Code:

**Core Agents:**
- `/analyst` - Market research, brainstorming, project briefs
- `/pm` - Product management, PRD creation, feature prioritization  
- `/architect` - System architecture design and technical specifications
- `/ux-expert` - Frontend specifications and UI design prompts
- `/po` - Product owner validation, epic management, story alignment
- `/sm` - Scrum master story drafting and sprint management
- `/dev` - Full-stack development and implementation
- `/qa` - Code review, refactoring, testing, quality assurance
- `/bmad-master` - Multi-role agent for any BMad task (context-heavy)
- `/bmad-orchestrator` - Heavy-weight orchestration agent (web use only)

**Task Commands:**
- `/create-next-story` - Generate development stories from epics
- `/shard-doc` - Break down PRD/architecture into focused documents
- `/validate-next-story` - Validate story against artifacts
- `/review-story` - Comprehensive story review process
- `/create-doc` - Create documentation from templates
- `/document-project` - Generate project documentation
- `/correct-course` - Project course correction analysis
- `/execute-checklist` - Run standardized checklists
- `/pdf-conversion-task` - Convert PDF documents to Markdown format

### Development Workflow

**Planning Phase (Web UI Recommended):**
1. Analyst research and project brief creation
2. PM creates PRD with functional/non-functional requirements
3. UX Expert creates frontend specifications (optional)
4. Architect designs system architecture
5. PO validates document alignment
6. Document sharding for development readiness

**Development Cycle (IDE):**
1. SM drafts next story from sharded epics
2. PO validates story (optional)
3. Dev implements tasks sequentially with testing
4. QA reviews and refactors code (optional)
5. User verification and testing validation
6. Commit changes and mark story complete

### Configuration Files

**Core Configuration:** `.bmad-core/core-config.yaml`
- Document locations and sharding settings
- Dev agent always-load files configuration
- Story and architecture file patterns

**Developer Context Files (Auto-loaded by /dev):**
- `docs/architecture/coding-standards.md`
- `docs/architecture/tech-stack.md` 
- `docs/architecture/source-tree.md`

### Key Development Commands

**Installation/Setup:**
```bash
# Install BMad-Method framework
npx bmad-method install --full --ide claude-code

# Check available expansion packs
npx bmad-method install --help
```

**Document Management:**
- Stories location: `docs/stories/`
- Debug logs: `.ai/debug-log.md`
- PRD location: `docs/prd.md` (sharded to `docs/prd/`)
- Architecture: `docs/architecture.md` (sharded to `docs/architecture/`)

### Agent Usage Patterns

**Sequential Development:**
1. Use `/sm` to draft stories from epics
2. Use `/dev` for implementation with auto-loaded standards
3. Use `/qa` for code review and refactoring
4. Commit frequently and run full test suites

**Context Management:**
- Agents load only required dependencies (lean context)
- Dev agent auto-loads project standards files
- Use appropriate agent for specific tasks
- Switch to `/bmad-master` for multi-role tasks

### Best Practices

**Development Standards:**
- Always run tests and linting before story completion
- Commit changes before marking stories complete
- Follow coding standards in auto-loaded files
- Maintain clean, focused file organization

**Agent Interaction:**
- Use numbered option lists for task selection
- Follow exact task workflows for dependency execution
- Interactive tasks (elicit=true) require user input
- Keep context lean by using appropriate specialized agents

### Technical Preferences

Customize agent behavior through `.bmad-core/data/technical-preferences.md` to bias technology selection and design patterns toward your preferences.

## PDF Document Ingestion

### Core Requirement: NO DIRECT PDF INGESTION
**CRITICAL**: All BMAD agents are configured to NEVER directly ingest PDF files. All PDFs must be converted to Markdown format before agent processing.

### PDF Conversion Pipeline

#### Automatic Conversion Process
1. **PDF Detection**: Agents automatically detect PDF file references
2. **Existing Check**: Search `input-documents-converted-to-md/` for existing conversions
3. **Version Selection**: Use latest version (highest `_v{n}` suffix)
4. **Auto-Convert**: Trigger conversion if no Markdown version exists
5. **Quality Validation**: Verify conversion meets quality thresholds
6. **Agent Handoff**: Process converted Markdown file

#### Directory Structure
```
input-documents/                    # Source PDFs (maintain hierarchy)
├── project-specs/
│   └── requirements.pdf
└── research/
    └── analysis.pdf

input-documents-converted-to-md/    # Converted MDs (mirror hierarchy)  
├── project-specs/
│   ├── requirements.md
│   └── requirements_v2.md         # Latest version used
└── research/
    └── analysis.md
```

#### Version Management
- **Base conversion**: `document.md`
- **Subsequent conversions**: `document_v2.md`, `document_v3.md`, etc.
- **Priority**: Agents always use highest numbered version
- **Automatic**: New conversions create next version number

### Conversion Commands

#### Manual Conversion
```bash
# Convert single PDF
python3 utilities/pdf-ingestion-pipeline/convert_pdf.py input-documents/document.pdf

# Batch convert all PDFs
./utilities/pdf-ingestion-pipeline/batch_converter.sh

# Force reconversion
python3 utilities/pdf-ingestion-pipeline/convert_pdf.py input-documents/document.pdf --force

# Get latest version path
python3 utilities/pdf-ingestion-pipeline/convert_pdf.py input-documents/document.pdf --latest
```

#### Validation Commands
```bash
# Validate single conversion
python3 utilities/validation-scripts/validate_conversion.py --file path/to/document.md

# Validate all conversions
python3 utilities/validation-scripts/validate_conversion.py --all

# Summary report only
python3 utilities/validation-scripts/validate_conversion.py --all --summary
```

### Agent Integration

#### PDF Reference Handling
- **Detection**: Agents scan user input for `.pdf` file references
- **Validation**: Check if source PDF exists in `input-documents/`
- **Conversion**: Auto-trigger conversion pipeline if needed  
- **Processing**: Reference converted Markdown file instead
- **Error Handling**: Graceful failure with user guidance

#### Configuration Integration
All agents load PDF ingestion rules from `docs/pdf-ingestion-rules.md` during startup, ensuring consistent behavior across the BMAD methodology.

### Error Handling
- **Conversion Failures**: Detailed logging, user notification, workflow halt
- **Quality Issues**: Warnings, manual review options, caution flags
- **Missing Files**: Specific error messages with file paths
- **Version Conflicts**: Automatic increment to next available version

### Usage Examples

#### Developer Workflow
```bash
# 1. Place PDF in source directory
cp project-requirements.pdf input-documents/specs/

# 2. Reference in agent interaction - auto-converts
/pm Create PRD based on input-documents/specs/project-requirements.pdf

# 3. Agent automatically uses: input-documents-converted-to-md/specs/project-requirements.md
```

#### Quality Assurance
```bash
# Validate conversion quality before important workflows  
python3 utilities/validation-scripts/validate_conversion.py --all
```

## Repository Template Usage

This repository serves as a template for BMad-Method projects. Clone and customize for new projects, ensuring the BMad framework is properly configured for your specific technology stack and requirements.