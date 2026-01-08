# Setup Guide

This guide will walk you through setting up the AI Code Review Assistant for your GitHub repository.

## Quick Start (5 minutes)

### 1. Fork or Clone Repository

```bash
git clone https://github.com/yourusername/iol-ai-code-review-yogesh.git
cd iol-ai-code-review-yogesh
```

### 2. Get API Keys

Choose one LLM provider and get an API key:

**OpenAI** (Recommended for beginners)
1. Go to https://platform.openai.com/api-keys
2. Create a new API key
3. Copy the key (starts with `sk-`)

**Anthropic**
1. Go to https://console.anthropic.com/
2. Create an API key
3. Copy the key (starts with `sk-ant-`)

**Azure OpenAI**
1. Create an Azure OpenAI resource
2. Get your API key and endpoint
3. Deploy a model (e.g., gpt-4)

### 3. Configure GitHub Repository

#### Add Secrets

1. Go to your GitHub repository
2. Navigate to: **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add the following secrets:

| Secret Name | Value | Required |
|-------------|-------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key | If using OpenAI |
| `ANTHROPIC_API_KEY` | Your Anthropic API key | If using Anthropic |
| `AZURE_OPENAI_API_KEY` | Your Azure API key | If using Azure |
| `AZURE_OPENAI_ENDPOINT` | Your Azure endpoint | If using Azure |
| `AZURE_OPENAI_DEPLOYMENT` | Your deployment name | If using Azure |
| `LLM_PROVIDER` | `openai`, `anthropic`, or `azure` | Optional (default: openai) |
| `LLM_MODEL` | Model name | Optional |

**Note**: `GITHUB_TOKEN` is automatically provided by GitHub Actions.

#### Copy Workflow File

The workflow file is already in `.github/workflows/ai-review.yml`. If you're setting up in a new repo:

```bash
mkdir -p .github/workflows
cp .github/workflows/ai-review.yml your-repo/.github/workflows/
```

### 4. Customize Configuration (Optional)

Edit `.ai-review.yaml` to customize the review behavior:

```yaml
# Example: Focus only on security and performance
focus_areas:
  code_quality: false
  security: true
  performance: true
  best_practices: false
  documentation: false

# Example: Block PR on critical issues
severity_config:
  block_pr_on_critical: true
```

### 5. Test the Setup

1. Create a test branch:
```bash
git checkout -b test-ai-review
```

2. Add a file with intentional issues:
```bash
cp sample_code/vulnerable_app.py test_file.py
git add test_file.py
git commit -m "Test: Add file with issues"
git push origin test-ai-review
```

3. Create a Pull Request on GitHub

4. Watch the AI reviewer in action! 🎉

## Detailed Configuration

### Environment Variables

For local testing, create a `.env` file:

```bash
cp .env.example .env
```

Edit `.env` with your values:

```env
GITHUB_TOKEN=ghp_your_personal_access_token
GITHUB_REPOSITORY=owner/repo
GITHUB_PR_NUMBER=1
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your-key-here
```

### GitHub Token Permissions

If using a personal access token (for local testing), ensure it has:
- `repo` scope (full control of private repositories)
- `write:discussion` (for posting comments)

For GitHub Actions, the default `GITHUB_TOKEN` has sufficient permissions if you set:

```yaml
permissions:
  contents: read
  pull-requests: write
```

### Configuration Options

#### Ignore Patterns

Ignore specific files or directories:

```yaml
ignore_patterns:
  - "*.md"
  - "*.txt"
  - "tests/**"
  - "vendor/**"
  - "node_modules/**"
  - "dist/**"
  - "build/**"
```

#### Custom Rules

Add project-specific rules:

```yaml
custom_rules:
  - name: "No TODO comments in production"
    pattern: "TODO:|FIXME:"
    severity: "warning"
    message: "TODO/FIXME comments should be resolved before merging"
  
  - name: "No console.log in production"
    pattern: "console\\.log\\("
    severity: "warning"
    message: "Remove console.log statements"
```

#### Language-Specific Settings

Configure per-language rules:

```yaml
language_specific:
  python:
    max_function_length: 50
    max_complexity: 10
    require_docstrings: true
  
  javascript:
    prefer_const: true
    no_var: true
  
  java:
    max_method_length: 50
    require_javadoc: true
```

## Local Development Setup

### Prerequisites

- Python 3.11+
- pip
- virtualenv (recommended)

### Setup Steps

1. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Install development dependencies**
```bash
pip install pytest pytest-cov black flake8 mypy
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your credentials
```

5. **Run tests**
```bash
pytest
```

6. **Run locally**
```bash
python -m src.main
```

## Docker Setup

### Build and Run

```bash
# Build image
docker build -t ai-code-reviewer .

# Run with environment file
docker run --env-file .env ai-code-reviewer

# Or with docker-compose
docker-compose up
```

### Docker Environment Variables

Create a `.env` file for Docker:

```env
GITHUB_TOKEN=your_token
GITHUB_REPOSITORY=owner/repo
GITHUB_PR_NUMBER=123
LLM_PROVIDER=openai
OPENAI_API_KEY=your_key
```

## Troubleshooting

### Common Issues

#### 1. "GitHub Token not found"

**Solution**: Ensure `GITHUB_TOKEN` is set in secrets (for Actions) or `.env` (for local).

#### 2. "LLM API error: Authentication failed"

**Solution**: 
- Check API key is correct
- Ensure no extra spaces in the key
- Verify the key has not expired

#### 3. "Failed to post comment"

**Solution**:
- Check GitHub token has `pull-requests: write` permission
- Verify the PR number is correct
- Check if the repository exists and is accessible

#### 4. "No comments posted"

**Possible reasons**:
- All files are in ignore patterns
- No issues found (good!)
- Severity threshold too high
- Check logs for errors

#### 5. "Rate limit exceeded"

**Solution**:
- Reduce `max_comments_per_file` and `max_total_comments`
- Wait for rate limit reset
- Use a different API key

### Debug Mode

Enable detailed logging:

```env
LOG_LEVEL=DEBUG
```

Or in `.ai-review.yaml`:

```yaml
log_level: DEBUG
```

### Testing Locally Without Creating PR

```bash
# Set environment variables
export GITHUB_TOKEN=your_token
export GITHUB_REPOSITORY=owner/repo
export GITHUB_PR_NUMBER=existing_pr_number
export OPENAI_API_KEY=your_key
export LLM_PROVIDER=openai

# Run in dry-run mode (modify main.py to skip posting)
python -m src.main
```

## Cost Estimation

### OpenAI Pricing (as of 2024)

| Model | Input (per 1M tokens) | Output (per 1M tokens) |
|-------|----------------------|------------------------|
| GPT-4 Turbo | $10 | $30 |
| GPT-3.5 Turbo | $0.50 | $1.50 |

### Typical PR Review Costs

- **Small PR** (1-3 files, <500 lines): $0.01 - $0.05
- **Medium PR** (5-10 files, <2000 lines): $0.10 - $0.30
- **Large PR** (20+ files, >5000 lines): $0.50 - $2.00

### Cost Optimization Tips

1. Use GPT-3.5 Turbo instead of GPT-4
2. Reduce `max_tokens` in configuration
3. Increase ignore patterns
4. Limit reviews to specific branches
5. Use static analysis only for less critical PRs

## Advanced Configuration

### Multiple Environments

Create environment-specific configs:

```bash
.ai-review.yaml          # Default
.ai-review.staging.yaml  # Staging
.ai-review.prod.yaml     # Production
```

Specify in workflow:

```yaml
env:
  CONFIG_FILE: .ai-review.prod.yaml
```

### Conditional Reviews

Review only specific file types:

```yaml
ignore_patterns:
  - "!*.py"  # Only review Python files
  - "!*.js"  # Only review JavaScript files
  - "*"      # Ignore everything else
```

### Team-Specific Rules

Create team-specific configurations:

```yaml
custom_rules:
  - name: "Use our logging library"
    pattern: "import logging"
    severity: "suggestion"
    message: "Use our custom logger: from utils.logger import get_logger"
```

## Next Steps

1. ✅ Complete setup
2. 📝 Customize configuration for your project
3. 🧪 Test with sample PRs
4. 🚀 Enable for all PRs
5. 📊 Monitor and adjust based on feedback
6. 🎯 Add custom rules for your codebase

## Support

If you encounter issues:
1. Check the [Known Limitations](README.md#known-limitations) section
2. Review logs in GitHub Actions
3. Open an issue on GitHub
4. Contact: yogesh@example.com
