# Source PDF Documents

This directory contains original PDF documents for BMAD agent ingestion.

## Structure
- Maintain any desired folder hierarchy
- Place PDF files here for conversion to Markdown
- Original hierarchy will be preserved in converted output

## Usage
1. Place PDF documents in this directory (with optional subdirectories)
2. BMAD agents will automatically detect and convert PDFs to Markdown
3. Converted files will appear in `../input-documents-converted-to-md/`

## Important Notes
- BMAD agents **never** directly ingest PDF files
- All PDFs must be converted to Markdown before agent processing
- Keep original PDFs here for reference and re-conversion if needed