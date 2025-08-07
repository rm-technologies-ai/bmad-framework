# Document Ingestion Workflow

## PDF-to-Markdown Conversion Workflow

### Overview
This workflow ensures all PDF documents are properly converted to Markdown format before BMAD agent ingestion, maintaining version control and quality validation throughout the process.

### Workflow Steps

#### 1. Document Reference Detection
```yaml
trigger: USER_REFERENCES_DOCUMENT
conditions:
  - document_path contains ".pdf"
  - file exists in input-documents/
actions:
  - log_pdf_reference_detected()
  - proceed_to_conversion_check()
```

#### 2. Existing Conversion Check
```yaml
input: pdf_file_path
process:
  - extract_relative_path_from_input_documents()
  - calculate_converted_file_location()
  - scan_for_existing_versions()
  - identify_latest_version()
output: 
  - existing_conversion_path OR null
  - version_number (if exists)
```

#### 3. Conversion Decision Matrix
```yaml
decision_logic:
  if existing_conversion_found:
    if force_reconvert_requested:
      -> trigger_new_conversion()
    else:
      -> use_existing_latest_version()
  else:
    -> trigger_new_conversion()
```

#### 4. PDF Conversion Process
```yaml
conversion_pipeline:
  input: 
    - source_pdf_path
    - target_markdown_path (with version)
  steps:
    - validate_pdf_accessibility()
    - determine_output_version_number()
    - create_output_directory_structure()
    - execute_conversion_script()
    - validate_conversion_output()
  error_handling:
    - log_conversion_errors()
    - notify_user_of_failure()
    - halt_agent_processing()
```

#### 5. Quality Validation
```yaml
validation_process:
  input: converted_markdown_path
  checks:
    - file_exists_and_readable()
    - minimum_content_length()
    - encoding_validation()
    - structure_analysis()
    - content_quality_score()
  thresholds:
    - min_length: 100 characters
    - min_quality_score: 40/100
    - required_encoding: utf-8
  outcomes:
    - PASS: proceed_with_ingestion()
    - FAIL: retry_conversion_or_error()
```

#### 6. Agent Integration Handoff
```yaml
final_steps:
  - update_document_references()
  - provide_converted_file_path_to_agent()
  - log_successful_ingestion()
  - proceed_with_agent_workflow()
```

### Error Handling Workflows

#### Conversion Failure Recovery
```yaml
on_conversion_failure:
  - log_detailed_error_information()
  - check_pdf_file_integrity()
  - verify_conversion_script_availability()
  - attempt_alternative_conversion_method()
  - if_all_methods_fail:
    - notify_user_with_specific_guidance()
    - halt_workflow_gracefully()
```

#### Quality Validation Failure
```yaml
on_quality_failure:
  - log_quality_scores_and_issues()
  - attempt_conversion_with_different_parameters()
  - if_retry_also_fails:
    - warn_user_about_quality_issues()
    - offer_manual_review_option()
    - proceed_with_caution_flag()
```

### Version Management Workflow

#### Version Number Assignment
```yaml
version_calculation:
  scan_pattern: "{basename}*.md"
  version_patterns:
    - "{basename}.md" -> version 1
    - "{basename}_v{n}.md" -> version n
  new_version_logic:
    - find_max_existing_version()
    - increment_by_one()
    - ensure_uniqueness()
```

#### Latest Version Resolution
```yaml
latest_version_selection:
  process:
    - list_all_versions_for_document()
    - extract_version_numbers()
    - select_highest_version()
    - return_full_path()
  priority_order:
    - "{basename}_v{highest_n}.md"
    - "{basename}.md" (if no versioned files)
```

### Integration Points

#### Agent Startup Integration
```yaml
startup_sequence:
  - load_core_config_document_ingestion()
  - initialize_conversion_pipeline_handlers()
  - validate_utility_script_availability()
  - set_up_error_handling_mechanisms()
  - mark_pdf_ingestion_workflow_ready()
```

#### Runtime Integration
```yaml
during_agent_execution:
  before_document_processing:
    - check_if_document_is_pdf()
    - if_pdf_trigger_conversion_workflow()
    - wait_for_conversion_completion()
    - use_converted_markdown_path()
  during_document_processing:
    - reference_only_markdown_files()
    - log_document_usage()
  after_document_processing:
    - update_usage_statistics()
```

### Configuration Dependencies

#### Required Configuration
```yaml
core_config_requirements:
  documentIngestion:
    pdfConversionRequired: true
    sourceDocumentsPath: input-documents
    convertedDocumentsPath: input-documents-converted-to-md
    pipelineScript: utilities/pdf-ingestion-pipeline/convert_pdf.py
    validationScript: utilities/validation-scripts/validate_conversion.py
    versioningEnabled: true
    latestVersionPriority: true
```

#### File Dependencies
- `utilities/pdf-to-md-converter/convert_pdf_to_md.py`
- `utilities/pdf-ingestion-pipeline/convert_pdf.py`
- `utilities/validation-scripts/validate_conversion.py`
- `docs/pdf-ingestion-rules.md`

### Performance Considerations

#### Optimization Strategies
- Cache conversion results to avoid repeated processing
- Batch conversion for multiple PDFs
- Asynchronous conversion for large files
- Quality validation caching

#### Resource Management
- Monitor disk space for converted documents
- Clean up failed conversion attempts
- Limit concurrent conversions
- Memory management for large PDF processing

### Monitoring and Logging

#### Key Metrics
- Conversion success rate
- Average conversion time
- Quality validation scores
- Error frequency by type

#### Log Entries
- PDF reference detection
- Conversion initiation and completion
- Quality validation results
- Error conditions and resolutions
- Agent handoff confirmations