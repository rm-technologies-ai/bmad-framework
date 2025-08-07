# /pdf-conversion-task Command

## PDF Conversion Task - Claude Code Integration

This task handles PDF-to-Markdown conversion using Claude Code's internal PDF processing capabilities.

### Task Definition

**Purpose**: Convert PDF documents to Markdown format using Claude's Read tool for direct PDF ingestion

**Trigger Conditions**:
- User references a PDF file
- PDF file detected in input-documents/
- Explicit conversion request

### Execution Steps

#### 1. PDF Detection and Validation
```yaml
input_validation:
  - check_pdf_file_exists_in_filesystem()
  - validate_pdf_path_format()
  - confirm_source_directory_location()
```

#### 2. Existing Conversion Check
```yaml
conversion_check:
  - scan_converted_directory_for_existing_md()
  - identify_existing_versions()
  - determine_latest_version_number()
  - report_conversion_status()
```

#### 3. Claude Code PDF Extraction
```yaml
conversion_process:
  when: no_existing_conversion OR force_reconvert
  actions:
    - use_read_tool_for_pdf_extraction()
    - format_extracted_content_as_markdown()
    - calculate_output_path_with_version()
    - write_markdown_file()
    - validate_conversion_quality()
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
2. If PDF: Use Read tool to extract PDF content directly
3. Format content as structured Markdown
4. Write to versioned file in input-documents-converted-to-md/
5. Proceed with agent workflow using converted file
```

#### Command Parameters
- `pdf_path`: Path to source PDF file
- `force_reconvert`: Boolean to force new conversion
- `quality_threshold`: Minimum quality score (optional)

### Claude Code Tool Integration

#### Required Tools
- `Read` - Claude Code's PDF processing tool
- `Write` - For creating converted Markdown files
- `LS` - For directory validation
- `Glob` - For finding existing conversions

#### Configuration Settings
```yaml
documentIngestion:
  pdfConversionMethod: claude_code_read_tool
  sourceDocumentsPath: input-documents
  convertedDocumentsPath: input-documents-converted-to-md
  latestVersionPriority: true
  autoVersionIncrement: true
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