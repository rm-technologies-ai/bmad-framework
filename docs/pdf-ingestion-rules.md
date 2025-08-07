# PDF Document Ingestion Rules

## MANDATORY PDF CONVERSION POLICY

### Core Rule: NO DIRECT PDF INGESTION
- **NEVER** ingest PDF files directly into BMAD agents
- **ALWAYS** convert PDFs to Markdown before agent processing
- **ALL** document references must use converted Markdown versions

### Conversion Requirements

#### 1. Automatic PDF Detection
- Agents must detect any PDF file references in user requests
- PDF references trigger immediate conversion validation
- Processing halts if PDF ingestion is attempted without conversion

#### 2. Conversion Validation Process
1. Check `input-documents-converted-to-md/` for existing conversion
2. If conversion exists: Use latest version (highest `_v{n}` suffix)
3. If no conversion: Trigger conversion pipeline automatically
4. Validate conversion quality before proceeding
5. Fail gracefully if conversion unsuccessful

#### 3. Version Management Rules
- Base conversion: `document.md`
- Subsequent conversions: `document_v2.md`, `document_v3.md`, etc.
- **ALWAYS** use highest numbered version when multiple exist
- Preserve original folder hierarchy from source PDFs

### File Path Conventions

#### Source Documents
```
input-documents/
├── project-specs/
│   └── requirements.pdf
├── research/
│   └── analysis.pdf
└── reference.pdf
```

#### Converted Documents
```
input-documents-converted-to-md/
├── project-specs/
│   ├── requirements.md
│   └── requirements_v2.md  # Latest version
├── research/
│   └── analysis.md
└── reference.md
```

### Agent Responsibilities

#### Pre-Processing Phase
1. **Scan user input** for PDF file references
2. **Check conversion status** for each referenced PDF
3. **Trigger conversion** if Markdown version missing or outdated
4. **Validate conversion quality** before proceeding
5. **Update file references** to point to converted Markdown

#### Error Handling
- **Conversion Failures**: Log detailed error, provide user guidance
- **Missing Source PDFs**: Error with specific file path
- **Quality Validation Failures**: Retry conversion, escalate if persistent
- **Version Conflicts**: Auto-increment to next available version

### Conversion Pipeline Integration

#### Automatic Conversion Trigger
```yaml
when: PDF_REFERENCE_DETECTED
actions:
  - validate_existing_conversion()
  - get_latest_version_path()
  - trigger_conversion_if_needed()
  - validate_conversion_quality()
  - update_file_references()
```

#### Quality Validation Criteria
- Minimum content length (>100 characters)
- Proper UTF-8 encoding
- Structured content (headers, formatting preserved)
- Text extraction accuracy score >80%

### Configuration Integration

#### Core Config Reference
```yaml
documentIngestion:
  pdfConversionRequired: true
  sourceDocumentsPath: input-documents
  convertedDocumentsPath: input-documents-converted-to-md
  latestVersionPriority: true
  validationRequired: true
```

#### Agent Loading Priority
1. Load PDF ingestion rules (this file)
2. Validate configuration settings
3. Initialize conversion pipeline handlers
4. Set up error handling mechanisms

### Compliance Enforcement

#### Agent Startup Checks
- [ ] PDF ingestion rules loaded
- [ ] Conversion pipeline accessible
- [ ] Validation scripts functional
- [ ] Error handling configured

#### Runtime Validation
- [ ] All document references checked for PDF format
- [ ] Conversion triggered automatically when needed
- [ ] Latest version priority enforced
- [ ] Quality validation performed

#### Failure Modes
- **Hard Fail**: Direct PDF ingestion attempts
- **Soft Fail**: Conversion quality issues (with user notification)
- **Retry**: Temporary conversion pipeline failures

### User Guidance

#### Expected Workflow
1. Place PDF documents in `input-documents/` directory
2. Reference documents in agent interactions (will auto-convert)
3. Work with Markdown versions in `input-documents-converted-to-md/`
4. Re-conversion automatically creates new versions

#### Error Messages
- "PDF ingestion not allowed. Converting to Markdown first..."
- "Conversion failed for [file]. Check PDF format and accessibility."
- "Using latest version: [file_v3.md] (converted from [original.pdf])"

### Maintenance Requirements

#### Regular Tasks
- Monitor conversion pipeline health
- Validate conversion quality periodically  
- Clean up old conversion versions (optional)
- Update conversion scripts as needed

#### Troubleshooting
- Check conversion script dependencies
- Verify file permissions and paths
- Validate PDF file integrity
- Test quality validation thresholds