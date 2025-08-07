# PDF Conversion Workflow - User Guide

## Overview

This guide explains how to work with PDF documents in the BMAD Method framework. All PDF documents must be converted to Markdown format before BMAD agents can process them.

## Key Principle: NO DIRECT PDF INGESTION

🚫 **BMAD agents NEVER directly ingest PDF files**  
✅ **All PDFs must be converted to Markdown first**  
🔄 **Conversion happens automatically when you reference PDFs**

## Quick Start

### 1. Place Your PDF Documents
Put your PDF files in the `input-documents/` directory:

```
input-documents/
├── project-requirements.pdf
├── research/
│   └── market-analysis.pdf
└── specs/
    └── technical-specs.pdf
```

### 2. Reference PDFs in Agent Interactions
When you reference a PDF, the agent will automatically convert it:

```bash
# This triggers automatic conversion
/pm Create PRD based on input-documents/project-requirements.pdf

# Agent converts PDF and uses the Markdown version
# Conversion appears in: input-documents-converted-to-md/project-requirements.md
```

### 3. Work with Converted Documents
BMAD agents always work with the converted Markdown files in `input-documents-converted-to-md/`.

## Directory Structure

### Source Documents (Your PDFs)
```
input-documents/                    # Place your PDF files here
├── project-specs/
│   ├── requirements.pdf           # Original PDF
│   └── architecture.pdf           # Original PDF  
├── research/
│   └── market-study.pdf            # Original PDF
└── contracts/
    └── vendor-agreement.pdf        # Original PDF
```

### Converted Documents (Auto-Generated)
```
input-documents-converted-to-md/    # Auto-generated Markdown files
├── project-specs/
│   ├── requirements.md            # First conversion
│   ├── requirements_v2.md         # Second conversion (latest)
│   ├── architecture.md            # First conversion
│   └── architecture_v2.md         # Second conversion (latest)
├── research/
│   └── market-study.md             # Converted file
└── contracts/
    └── vendor-agreement.md         # Converted file
```

## Version Management

### How Versioning Works

1. **First conversion**: `document.md`
2. **Second conversion**: `document_v2.md` 
3. **Third conversion**: `document_v3.md`
4. **And so on...**

### Latest Version Priority
BMAD agents always use the **highest numbered version**:
- If you have `requirements.md` and `requirements_v3.md`, agents use `requirements_v3.md`
- Version numbers increment automatically with each new conversion

### When New Versions Are Created
- When you modify the source PDF and trigger reconversion
- When you manually force reconversion with `--force` flag
- Each conversion creates a new version (original files are preserved)

## Manual Conversion Commands

### Convert Single PDF
```bash
# Basic conversion
python3 utilities/pdf-ingestion-pipeline/convert_pdf.py input-documents/document.pdf

# Force reconversion (creates new version)
python3 utilities/pdf-ingestion-pipeline/convert_pdf.py input-documents/document.pdf --force

# Check latest version path without converting
python3 utilities/pdf-ingestion-pipeline/convert_pdf.py input-documents/document.pdf --latest
```

### Batch Convert All PDFs
```bash
# Convert all PDFs in input-documents/
./utilities/pdf-ingestion-pipeline/batch_converter.sh
```

### Validate Conversion Quality
```bash
# Validate single converted file
python3 utilities/validation-scripts/validate_conversion.py --file input-documents-converted-to-md/document.md

# Validate all conversions
python3 utilities/validation-scripts/validate_conversion.py --all

# Quick summary report
python3 utilities/validation-scripts/validate_conversion.py --all --summary
```

## Agent Workflow Integration

### Automatic Process
When you reference a PDF in any agent interaction:

1. **PDF Detection**: Agent detects `.pdf` in your request
2. **Conversion Check**: Looks for existing conversion in `input-documents-converted-to-md/`
3. **Version Selection**: Uses latest version if multiple exist
4. **Auto-Convert**: Converts PDF if no Markdown version exists
5. **Quality Check**: Validates conversion meets quality standards
6. **Processing**: Agent works with converted Markdown file

### Example Agent Interactions

#### Project Manager (PM) Agent
```bash
# You type this:
/pm Create product requirements based on input-documents/client-brief.pdf

# Agent automatically:
# 1. Detects client-brief.pdf
# 2. Converts to input-documents-converted-to-md/client-brief.md
# 3. Creates PRD using the converted Markdown content
```

#### Architect Agent
```bash
# You type this:
/architect Design system based on input-documents/specs/technical-requirements.pdf

# Agent automatically:  
# 1. Converts technical-requirements.pdf to Markdown
# 2. Creates architecture using converted content
```

### Manual Agent Control
```bash
# Force reconversion before agent processing
python3 utilities/pdf-ingestion-pipeline/convert_pdf.py input-documents/document.pdf --force

# Then use with agent
/dev Implement features from input-documents/document.pdf
```

## Quality Standards

### Conversion Quality Metrics
- **Minimum Content Length**: 100+ characters
- **Encoding**: Valid UTF-8
- **Structure**: Preserves headers, formatting
- **Quality Score**: 40+ out of 100 points

### Quality Validation Process
1. **Automatic**: Every conversion is validated automatically
2. **Manual**: Run validation commands to check quality
3. **Warnings**: Low quality scores generate user warnings
4. **Failures**: Poor quality conversions halt agent processing

### Improving Conversion Quality
- Ensure PDF is text-based (not scanned images)
- Use high-quality, well-formatted source PDFs
- Check that PDF is not password-protected or corrupted
- Consider manual cleanup of converted Markdown if needed

## Error Handling

### Common Error Scenarios

#### PDF File Not Found
```
Error: PDF file not found: input-documents/missing-file.pdf
Solution: Check file path and ensure PDF is in input-documents/
```

#### Conversion Failed  
```
Error: PDF conversion failed: [specific error]
Solutions:
- Check PDF is not corrupted or password-protected
- Verify PDF contains extractable text (not just images)
- Check conversion script dependencies
```

#### Quality Validation Failed
```
Warning: Conversion quality score too low (25/100)
Solutions:
- Review converted Markdown manually
- Try reconversion with --force flag
- Consider manual cleanup of converted file
- Check source PDF quality
```

#### Permission Issues
```
Error: Cannot write to input-documents-converted-to-md/
Solutions:  
- Check directory write permissions
- Ensure directories exist and are accessible
```

### Troubleshooting Steps

1. **Check File Paths**
   - Verify PDF exists in `input-documents/`
   - Check correct relative path structure

2. **Validate PDF Quality**  
   - Open PDF manually to verify it's readable
   - Ensure PDF contains text (not just images)
   - Check PDF is not password-protected

3. **Test Conversion Scripts**
   ```bash
   # Test basic conversion
   python3 utilities/pdf-to-md-converter/convert_pdf_to_md.py --help
   
   # Test pipeline script
   python3 utilities/pdf-ingestion-pipeline/convert_pdf.py --help
   ```

4. **Review Conversion Quality**
   ```bash
   # Check conversion results
   python3 utilities/validation-scripts/validate_conversion.py --all
   ```

## Best Practices

### Organizing Your PDFs
- **Use Clear Folder Structure**: Organize PDFs logically in `input-documents/`
- **Meaningful Filenames**: Use descriptive names without special characters
- **Consistent Naming**: Follow consistent naming conventions

### Working with Conversions  
- **Check Quality First**: Validate conversions before important workflows
- **Review Critical Documents**: Manually review converted Markdown for critical PDFs
- **Version Control**: Keep track of which version agents are using
- **Regular Validation**: Run periodic quality checks

### Agent Interaction
- **Reference by Path**: Always reference PDFs with full path from `input-documents/`
- **Let Agents Convert**: Don't manually convert unless needed - let agents handle it
- **Check Latest Versions**: Be aware which version agents are using

### Maintenance
- **Clean Up Old Versions**: Periodically remove old conversion versions if needed
- **Monitor Disk Space**: Conversions create additional files
- **Update Scripts**: Keep conversion scripts updated for best quality

## Advanced Usage

### Custom Conversion Parameters
```bash  
# Force high-quality conversion (customize as needed)
python3 utilities/pdf-ingestion-pipeline/convert_pdf.py input-documents/document.pdf --force --quality-threshold 80
```

### Bulk Operations
```bash
# Convert all PDFs and validate
./utilities/pdf-ingestion-pipeline/batch_converter.sh
python3 utilities/validation-scripts/validate_conversion.py --all --summary
```

### Integration with Git
```bash
# Add converted files to git (optional)
git add input-documents-converted-to-md/
git commit -m "Update PDF conversions"

# Or ignore converted files (add to .gitignore)
echo "input-documents-converted-to-md/" >> .gitignore
```

## Support

### Getting Help
- **Check Logs**: Review conversion and validation logs for detailed errors
- **Test Scripts**: Verify utility scripts are working correctly
- **Validate Config**: Ensure `.bmad-core/core-config.yaml` is properly configured
- **Review Rules**: Check `docs/pdf-ingestion-rules.md` for policy details

### Reporting Issues  
- Note exact error messages
- Include PDF file details (size, source, type)
- Provide conversion command used
- Include validation results if available