#!/bin/bash
# Test Runner for PDF Ingestion Pipeline
# Comprehensive testing and validation script

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}PDF Ingestion Pipeline - Test Suite${NC}"
echo "========================================"
echo

# Function to print section headers
print_section() {
    echo -e "\n${BLUE}$1${NC}"
    echo "----------------------------------------"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to run test and report result
run_test() {
    local test_name="$1"
    local test_command="$2"
    
    echo -n "Testing $test_name... "
    
    if eval "$test_command" >/dev/null 2>&1; then
        echo -e "${GREEN}PASS${NC}"
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        return 1
    fi
}

# Initialize counters
TOTAL_TESTS=0
PASSED_TESTS=0

# Test 1: Check Python availability
print_section "Environment Tests"
TOTAL_TESTS=$((TOTAL_TESTS + 1))
if command_exists python3; then
    echo -e "Python 3: ${GREEN}Available${NC}"
    PASSED_TESTS=$((PASSED_TESTS + 1))
else
    echo -e "Python 3: ${RED}Missing${NC}"
fi

# Test 2: Check directory structure
print_section "Directory Structure Tests"

directories=(
    "input-documents"
    "input-documents-converted-to-md"
    "utilities/pdf-ingestion-pipeline"
    "utilities/validation-scripts"
    "utilities/pdf-to-md-converter"
    ".bmad-core"
    ".claude"
    "docs"
)

for dir in "${directories[@]}"; do
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    if [ -d "$dir" ]; then
        echo -e "$dir: ${GREEN}EXISTS${NC}"
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        echo -e "$dir: ${RED}MISSING${NC}"
    fi
done

# Test 3: Check required files
print_section "Required Files Tests"

files=(
    "utilities/pdf-ingestion-pipeline/convert_pdf.py"
    "utilities/validation-scripts/validate_conversion.py"
    "utilities/pdf-to-md-converter/convert_pdf_to_md.py"
    "utilities/pdf-ingestion-pipeline/batch_converter.sh"
    ".bmad-core/core-config.yaml"
    "docs/pdf-ingestion-rules.md"
    "PDF_CONVERSION_WORKFLOW.md"
    "IMPLEMENTATION_PLAN.md"
)

for file in "${files[@]}"; do
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    if [ -f "$file" ]; then
        echo -e "$file: ${GREEN}EXISTS${NC}"
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        echo -e "$file: ${RED}MISSING${NC}"
    fi
done

# Test 4: Check executable permissions
print_section "Executable Permissions Tests"

executables=(
    "utilities/pdf-ingestion-pipeline/batch_converter.sh"
)

for exe in "${executables[@]}"; do
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    if [ -x "$exe" ]; then
        echo -e "$exe: ${GREEN}EXECUTABLE${NC}"
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        echo -e "$exe: ${RED}NOT EXECUTABLE${NC}"
    fi
done

# Test 5: Script functionality tests
print_section "Script Functionality Tests"

# Test converter help
TOTAL_TESTS=$((TOTAL_TESTS + 1))
if python3 utilities/pdf-ingestion-pipeline/convert_pdf.py --help >/dev/null 2>&1; then
    echo -e "Converter help: ${GREEN}WORKING${NC}"
    PASSED_TESTS=$((PASSED_TESTS + 1))
else
    echo -e "Converter help: ${RED}FAILED${NC}"
fi

# Test validation help
TOTAL_TESTS=$((TOTAL_TESTS + 1))
if python3 utilities/validation-scripts/validate_conversion.py --help >/dev/null 2>&1; then
    echo -e "Validation help: ${GREEN}WORKING${NC}"
    PASSED_TESTS=$((PASSED_TESTS + 1))
else
    echo -e "Validation help: ${RED}FAILED${NC}"
fi

# Test 6: Configuration tests
print_section "Configuration Tests"

# Check core config contains required sections
TOTAL_TESTS=$((TOTAL_TESTS + 1))
if grep -q "documentIngestion:" .bmad-core/core-config.yaml 2>/dev/null; then
    echo -e "Core config - documentIngestion: ${GREEN}FOUND${NC}"
    PASSED_TESTS=$((PASSED_TESTS + 1))
else
    echo -e "Core config - documentIngestion: ${RED}MISSING${NC}"
fi

TOTAL_TESTS=$((TOTAL_TESTS + 1))
if grep -q "pdfConversionRequired: true" .bmad-core/core-config.yaml 2>/dev/null; then
    echo -e "Core config - pdfConversionRequired: ${GREEN}FOUND${NC}"
    PASSED_TESTS=$((PASSED_TESTS + 1))
else
    echo -e "Core config - pdfConversionRequired: ${RED}MISSING${NC}"
fi

# Test 7: Agent integration tests
print_section "Agent Integration Tests"

agent_files=(
    ".bmad-core/agents/dev.md"
    ".bmad-core/agents/pm.md"
    ".claude/commands/BMad/agents/dev.md"
    ".claude/commands/BMad/agents/pm.md"
)

for agent_file in "${agent_files[@]}"; do
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    if [ -f "$agent_file" ] && grep -q "documentIngestionRules:" "$agent_file" 2>/dev/null; then
        echo -e "$agent_file: ${GREEN}RULES FOUND${NC}"
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        echo -e "$agent_file: ${RED}RULES MISSING${NC}"
    fi
done

# Test 8: Run Python unit tests if available
print_section "Unit Tests"

TOTAL_TESTS=$((TOTAL_TESTS + 1))
if [ -f "utilities/validation-scripts/test_pipeline.py" ]; then
    echo "Running Python unit tests..."
    if python3 utilities/validation-scripts/test_pipeline.py; then
        echo -e "Unit tests: ${GREEN}PASSED${NC}"
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        echo -e "Unit tests: ${RED}FAILED${NC}"
    fi
else
    echo -e "Unit tests: ${YELLOW}NOT FOUND${NC}"
fi

# Test 9: Sample workflow test (if input files exist)
print_section "Workflow Tests"

TOTAL_TESTS=$((TOTAL_TESTS + 1))
if [ -n "$(find input-documents -name '*.pdf' 2>/dev/null)" ]; then
    echo "Found PDF files - testing conversion workflow..."
    if python3 utilities/validation-scripts/validate_conversion.py --all --summary >/dev/null 2>&1; then
        echo -e "Workflow test: ${GREEN}PASSED${NC}"
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        echo -e "Workflow test: ${RED}FAILED${NC}"
    fi
else
    echo -e "Workflow test: ${YELLOW}SKIPPED (no PDF files)${NC}"
    # Don't count this as a failure
    TOTAL_TESTS=$((TOTAL_TESTS - 1))
fi

# Final summary
print_section "Test Summary"

echo "Total Tests: $TOTAL_TESTS"
echo -e "Passed: ${GREEN}$PASSED_TESTS${NC}"
echo -e "Failed: ${RED}$((TOTAL_TESTS - PASSED_TESTS))${NC}"

PASS_RATE=$((PASSED_TESTS * 100 / TOTAL_TESTS))
echo "Pass Rate: $PASS_RATE%"

echo
if [ $PASSED_TESTS -eq $TOTAL_TESTS ]; then
    echo -e "${GREEN}✅ ALL TESTS PASSED! PDF ingestion pipeline is ready.${NC}"
    exit 0
elif [ $PASS_RATE -ge 80 ]; then
    echo -e "${YELLOW}⚠️  Most tests passed. Minor issues detected.${NC}"
    exit 1
else
    echo -e "${RED}❌ Multiple test failures. Pipeline needs attention.${NC}"
    exit 2
fi