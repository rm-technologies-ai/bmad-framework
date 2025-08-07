# Converted Markdown Documents

This directory contains Markdown versions of PDF documents converted for BMAD agent ingestion.

## Structure
- Mirrors the folder hierarchy of `../input-documents/`
- Contains `.md` files converted from source PDFs
- Version-controlled with numerical suffixes (e.g., `document_v2.md`)

## Version Management
- Base conversion: `document.md`
- Subsequent conversions: `document_v2.md`, `document_v3.md`, etc.
- BMAD agents always use the **highest numbered version**

## Usage
- BMAD agents automatically reference files from this directory
- Files are created automatically during PDF conversion process
- Do not manually edit converted files - re-convert source PDFs instead

## Important Notes
- This directory is managed automatically by the PDF ingestion pipeline
- BMAD agents only ingest Markdown files from this location
- Latest version priority ensures agents use most recent conversions