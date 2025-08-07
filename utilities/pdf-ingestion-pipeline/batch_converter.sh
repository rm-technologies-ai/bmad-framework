#!/bin/bash
# Batch PDF Conversion Script
# Converts all PDFs in input-documents directory to Markdown

# Configuration
INPUT_DIR="input-documents"
CONVERTER_SCRIPT="utilities/pdf-ingestion-pipeline/convert_pdf.py"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}BMAD PDF Batch Converter${NC}"
echo "=============================="

# Check if input directory exists
if [ ! -d "$INPUT_DIR" ]; then
    echo -e "${RED}Error: Input directory '$INPUT_DIR' not found${NC}"
    exit 1
fi

# Check if converter script exists
if [ ! -f "$CONVERTER_SCRIPT" ]; then
    echo -e "${RED}Error: Converter script '$CONVERTER_SCRIPT' not found${NC}"
    exit 1
fi

# Find all PDF files
PDF_FILES=$(find "$INPUT_DIR" -name "*.pdf" -type f)

if [ -z "$PDF_FILES" ]; then
    echo -e "${BLUE}No PDF files found in $INPUT_DIR${NC}"
    exit 0
fi

# Count files
PDF_COUNT=$(echo "$PDF_FILES" | wc -l)
echo -e "${BLUE}Found $PDF_COUNT PDF file(s) to convert${NC}"
echo

# Convert each file
SUCCESS_COUNT=0
FAIL_COUNT=0

while IFS= read -r pdf_file; do
    echo -e "${BLUE}Processing: $pdf_file${NC}"
    
    if python3 "$CONVERTER_SCRIPT" "$pdf_file"; then
        echo -e "${GREEN}✓ Success${NC}"
        ((SUCCESS_COUNT++))
    else
        echo -e "${RED}✗ Failed${NC}"
        ((FAIL_COUNT++))
    fi
    echo
done <<< "$PDF_FILES"

# Summary
echo "=============================="
echo -e "${GREEN}Successful conversions: $SUCCESS_COUNT${NC}"
echo -e "${RED}Failed conversions: $FAIL_COUNT${NC}"
echo -e "${BLUE}Total files processed: $((SUCCESS_COUNT + FAIL_COUNT))${NC}"

exit 0