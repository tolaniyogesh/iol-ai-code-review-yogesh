#!/bin/bash

# Local execution script for AI Code Review Assistant
# Usage: ./run_local.sh <pr_number>

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}AI Code Review Assistant - Local Runner${NC}"
echo "========================================"

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${RED}Error: .env file not found${NC}"
    echo "Please create .env file from .env.example"
    exit 1
fi

# Load environment variables
source .env

# Check if PR number is provided
if [ -z "$1" ]; then
    if [ -z "$GITHUB_PR_NUMBER" ]; then
        echo -e "${RED}Error: PR number not provided${NC}"
        echo "Usage: ./run_local.sh <pr_number>"
        echo "Or set GITHUB_PR_NUMBER in .env file"
        exit 1
    fi
else
    export GITHUB_PR_NUMBER=$1
fi

# Check required environment variables
if [ -z "$GITHUB_TOKEN" ]; then
    echo -e "${RED}Error: GITHUB_TOKEN not set${NC}"
    exit 1
fi

if [ -z "$GITHUB_REPOSITORY" ]; then
    echo -e "${RED}Error: GITHUB_REPOSITORY not set${NC}"
    exit 1
fi

# Check if at least one LLM API key is set
if [ -z "$OPENAI_API_KEY" ] && [ -z "$ANTHROPIC_API_KEY" ] && [ -z "$AZURE_OPENAI_API_KEY" ]; then
    echo -e "${RED}Error: No LLM API key found${NC}"
    echo "Please set one of: OPENAI_API_KEY, ANTHROPIC_API_KEY, or AZURE_OPENAI_API_KEY"
    exit 1
fi

echo -e "${GREEN}Configuration:${NC}"
echo "Repository: $GITHUB_REPOSITORY"
echo "PR Number: $GITHUB_PR_NUMBER"
echo "LLM Provider: ${LLM_PROVIDER:-openai}"
echo "Model: ${LLM_MODEL:-gpt-4-turbo-preview}"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Virtual environment not found. Creating...${NC}"
    python -m venv venv
fi

# Activate virtual environment
echo -e "${GREEN}Activating virtual environment...${NC}"
source venv/bin/activate

# Install dependencies
echo -e "${GREEN}Installing dependencies...${NC}"
pip install -q -r requirements.txt

# Run the reviewer
echo -e "${GREEN}Starting code review...${NC}"
echo ""
python -m src.main

# Check exit code
if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✓ Review completed successfully${NC}"
else
    echo ""
    echo -e "${RED}✗ Review failed${NC}"
    exit 1
fi
