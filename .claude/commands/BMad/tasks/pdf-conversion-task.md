# /pdf-conversion-task Command

## PDF Conversion Task for Claude Integration

This task handles PDF-to-Markdown conversion within the Claude environment.

### Task Definition

**Purpose**: Convert PDF documents to Markdown format for BMAD agent ingestion

**Trigger Conditions**:
- User references a PDF file
- PDF file detected in input-documents/
- Explicit conversion request

### Execution Steps

#### 1. PDF Detection and Validation
```yaml
input_validation:
  - check_pdf_file_exists()
  - validate_pdf_accessibility()
  - confirm_source_directory_location()
```

#### 2. Existing Conversion Check
```yaml
conversion_check:
  - scan_converted_directory()
  - identify_existing_versions()
  - determine_latest_version()
  - report_conversion_status()
```

#### 3. Conversion Execution
```yaml
conversion_process:
  when: no_existing_conversion OR force_reconvert
  actions:
    - calculate_output_path_with_version()
    - execute_conversion_pipeline()
    - validate_conversion_quality()
    - report_conversion_results()
```

#### 4. Quality Validation
```yaml
quality_checks:
  - minimum_content_length_check()
  - encoding_validation()
  - structure_analysis()
  - content_quality_scoring()
  thresholds:
    min_length: 100
    min_quality_score: 40
```

#### 5. Result Handoff
```yaml
completion:
  on_success:
    - return_converted_file_path()
    - log_successful_conversion()
    - proceed_with_agent_workflow()
  on_failure:
    - log_conversion_error()
    - provide_user_guidance()
    - halt_agent_processing()
```

### Error Handling

#### Conversion Failures
- Log detailed error information
- Check PDF file integrity
- Verify conversion script availability
- Provide specific user guidance
- Halt workflow gracefully

#### Quality Validation Issues
- Warn about quality concerns
- Offer manual review option
- Proceed with caution flags
- Log quality metrics

### Integration with Claude Commands

#### Usage in Agent Commands
```markdown
When processing documents:
1. Check if document is PDF format
2. If PDF: execute /pdf-conversion-task
3. Wait for conversion completion
4. Use converted Markdown path
5. Proceed with agent workflow
```

#### Command Parameters
- `pdf_path`: Path to source PDF file
- `force_reconvert`: Boolean to force new conversion
- `quality_threshold`: Minimum quality score (optional)

### Configuration Dependencies

#### Required Files
- `utilities/pdf-to-md-converter/convert_pdf_to_md.py`
- `utilities/pdf-ingestion-pipeline/convert_pdf.py`
- `utilities/validation-scripts/validate_conversion.py`
- `docs/pdf-ingestion-rules.md`

#### Configuration Settings
```yaml
documentIngestion:
  pdfConversionRequired: true
  sourceDocumentsPath: input-documents
  convertedDocumentsPath: input-documents-converted-to-md
  latestVersionPriority: true
```

### Output Format

#### Success Response
```yaml
status: success
converted_file: input-documents-converted-to-md/path/to/document_v2.md
original_file: input-documents/path/to/document.pdf
version: 2
quality_score: 85
```

#### Error Response
```yaml
status: error
error_type: conversion_failed
error_message: "PDF conversion failed: [specific error]"
original_file: input-documents/path/to/document.pdf
troubleshooting: "Check PDF format and accessibility"
```