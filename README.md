# 🤖 AI Code Review Assistant

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![GitHub Actions](https://img.shields.io/badge/CI-GitHub%20Actions-blue)](https://github.com/features/actions)

An intelligent, automated code review assistant that analyzes pull requests and provides actionable, context-aware feedback using AI. Supports multiple LLM providers (OpenAI, Anthropic, Azure OpenAI) and integrates seamlessly with GitHub.

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [GitHub Actions Setup](#-github-actions-setup)
- [Docker Deployment](#-docker-deployment)
- [Configuration Schema](#-configuration-schema)
- [Sample PR](#-sample-pr)
- [Testing](#-testing)
- [Known Limitations](#-known-limitations)
- [Future Improvements](#-future-improvements)
- [License](#-license)

## ✨ Features

### Core Capabilities

- **🔍 Multi-Layer Analysis**
  - Static code analysis for immediate issue detection
  - AI-powered contextual review using LLMs
  - Pattern-based security vulnerability detection
  - Performance bottleneck identification

- **🎯 Smart Review Comments**
  - Severity-based categorization (🔴 Critical, 🟡 Warning, 🔵 Suggestion)
  - Line-specific feedback with exact references
  - Actionable suggestions with code fixes
  - Context-aware analysis avoiding obvious comments

- **🔌 Multi-Provider LLM Support**
  - OpenAI (GPT-4, GPT-3.5)
  - Anthropic (Claude 3)
  - Azure OpenAI
  - **Google Gemini (FREE!)** - No credit card required
  - Configurable model selection

- **⚙️ Highly Configurable**
  - Custom ignore patterns
  - Focus area selection (security, performance, quality, etc.)
  - Severity thresholds for PR blocking
  - Custom pattern-based rules
  - Language-specific configurations

- **🚀 Easy Integration**
  - GitHub Actions workflow included
  - Docker containerized deployment
  - Automatic PR comment posting
  - Review summary generation

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     GitHub Pull Request                      │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              GitHub Actions Workflow Trigger                 │
│                  (on PR open/update)                         │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   AI Code Reviewer                           │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  1. Configuration Loader                             │   │
│  │     - Load .ai-review.yaml                           │   │
│  │     - Parse environment variables                    │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  2. GitHub Client                                    │   │
│  │     - Fetch PR details & file changes                │   │
│  │     - Get file contents                              │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  3. Static Analyzer                                  │   │
│  │     - Pattern matching (security, quality)           │   │
│  │     - Language-specific checks                       │   │
│  │     - Custom rule evaluation                         │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  4. AI Analyzer                                      │   │
│  │     - LLM Provider (OpenAI/Anthropic/Azure)          │   │
│  │     - Context-aware code review                      │   │
│  │     - Intelligent suggestion generation              │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  5. Comment Aggregator & Filter                     │   │
│  │     - Deduplication                                  │   │
│  │     - Severity filtering                             │   │
│  │     - Comment limiting                               │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  6. GitHub Comment Poster                            │   │
│  │     - Post inline comments                           │   │
│  │     - Generate review summary                        │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│           Review Comments Posted on GitHub PR                │
└─────────────────────────────────────────────────────────────┘
```

### Component Description

| Component | Responsibility |
|-----------|---------------|
| **Configuration Loader** | Parses YAML config and environment variables |
| **GitHub Client** | Interfaces with GitHub API for PR operations |
| **Static Analyzer** | Performs pattern-based code analysis |
| **AI Analyzer** | Uses LLMs for intelligent code review |
| **Comment Aggregator** | Filters, deduplicates, and prioritizes comments |
| **GitHub Poster** | Posts formatted comments to PR |

## 📦 Prerequisites

- **Python 3.11+**
- **GitHub Account** with repository access
- **LLM API Key** (at least one):
  - OpenAI API key
  - Anthropic API key
  - Azure OpenAI credentials
- **Docker** (optional, for containerized deployment)

## 🚀 Installation

### Local Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/iol-ai-code-review-yogesh.git
cd iol-ai-code-review-yogesh
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your credentials
```

### Docker Setup

```bash
docker build -t ai-code-reviewer .
docker-compose up
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```env
# GitHub Configuration
GITHUB_TOKEN=ghp_your_github_token_here
GITHUB_REPOSITORY=owner/repo
GITHUB_PR_NUMBER=1

# LLM Provider Selection
LLM_PROVIDER=openai  # Options: openai, anthropic, azure

# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-key

# Anthropic Configuration
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key

# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your-azure-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=your-deployment-name

# LLM Settings
LLM_MODEL=gpt-4-turbo-preview
LLM_MAX_TOKENS=4096
LLM_TEMPERATURE=0.3

# Application Settings
CONFIG_FILE=.ai-review.yaml
LOG_LEVEL=INFO
```

### Review Configuration (.ai-review.yaml)

```yaml
version: "1.0"
enabled: true

# Files/directories to ignore
ignore_patterns:
  - "*.md"
  - "*.txt"
  - "tests/**"
  - "docs/**"

# Focus areas for review
focus_areas:
  code_quality: true
  security: true
  performance: true
  best_practices: true
  documentation: true

# Severity configuration
severity_config:
  block_pr_on_critical: false
  block_pr_on_warning: false
  min_severity_to_comment: "suggestion"

# Review behavior
review_settings:
  max_comments_per_file: 10
  max_total_comments: 50
  avoid_obvious_comments: true
  suggest_fixes: true
  include_line_numbers: true

# Custom pattern-based rules
custom_rules:
  - name: "No hardcoded credentials"
    pattern: "(password|api_key|secret)\\s*=\\s*['\"][^'\"]+['\"]"
    severity: "critical"
    message: "Hardcoded credentials detected. Use environment variables."

# Language-specific settings
language_specific:
  python:
    max_function_length: 50
    max_complexity: 10
    require_docstrings: true
  javascript:
    prefer_const: true
    no_var: true
```

**Note:** LLM configuration (provider, model, API keys) is set via environment variables or GitHub secrets, not in this file.

## 💻 Usage

### Local Execution

```bash
# Set environment variables
export GITHUB_TOKEN=your_token
export GITHUB_REPOSITORY=owner/repo
export GITHUB_PR_NUMBER=123
export OPENAI_API_KEY=your_key
export LLM_PROVIDER=openai

# Run the reviewer
python -m src.main
```

### Docker Execution

```bash
# Using docker-compose
docker-compose run ai-code-reviewer

# Using docker directly
docker run --env-file .env ai-code-reviewer
```

## 🔄 GitHub Actions Setup

### Step 1: Add Secrets to Repository

Go to your GitHub repository → Settings → Secrets and variables → Actions

Add the following secrets:
- `OPENAI_API_KEY` (or `ANTHROPIC_API_KEY` or Azure credentials)
- Optionally: `LLM_PROVIDER`, `LLM_MODEL`

**Note:** `GITHUB_TOKEN` is automatically provided by GitHub Actions.

### Step 2: Workflow File

The workflow file is already included at `.github/workflows/ai-review.yml`:

```yaml
name: AI Code Review

on:
  pull_request:
    types: [opened, synchronize, reopened]
    branches:
      - main
      - develop

permissions:
  contents: read
  pull-requests: write

jobs:
  ai-code-review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: python -m src.main
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          # ... other env vars
```

### Step 3: Create a Pull Request

Once configured, the AI reviewer will automatically run on every PR!

## 🐳 Docker Deployment

### Build Image

```bash
docker build -t ai-code-reviewer:latest .
```

### Run Container

```bash
docker run \
  -e GITHUB_TOKEN=$GITHUB_TOKEN \
  -e GITHUB_REPOSITORY=owner/repo \
  -e GITHUB_PR_NUMBER=123 \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  -e LLM_PROVIDER=openai \
  ai-code-reviewer:latest
```

### Docker Compose

```bash
# Start service
docker-compose up

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop service
docker-compose down
```

## 📊 Configuration Schema

The complete JSON schema is available in `config-schema.json`. Key configuration options:

| Option | Type | Description | Default |
|--------|------|-------------|---------|
| `enabled` | boolean | Enable/disable reviews | `true` |
| `ignore_patterns` | array | Glob patterns to ignore | `["*.md"]` |
| `focus_areas.*` | boolean | Enable specific review areas | `true` |
| `severity_config.block_pr_on_critical` | boolean | Block PR on critical issues | `false` |
| `review_settings.max_comments_per_file` | integer | Max comments per file | `10` |
| `custom_rules` | array | Custom pattern rules | `[]` |

## 🧪 Sample PR

The repository includes sample code with intentional issues in the `sample_code/` directory:

- **`vulnerable_app.py`**: Security vulnerabilities (SQL injection, hardcoded secrets, eval usage)
- **`bad_practices.js`**: Code quality issues (var usage, console.log, loose equality)
- **`performance_issues.py`**: Performance problems (N+1 queries, inefficient algorithms)

### Creating a Test PR

1. Create a new branch:
```bash
git checkout -b test-review
```

2. Modify or add files from `sample_code/`

3. Commit and push:
```bash
git add .
git commit -m "Test: Add code with intentional issues"
git push origin test-review
```

4. Create a PR on GitHub and watch the AI reviewer in action!

## 🧪 Testing

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_static_analyzer.py

# Run with verbose output
pytest -v
```

### Test Structure

```
tests/
├── __init__.py
├── test_static_analyzer.py  # Static analysis tests
└── test_config.py            # Configuration tests
```

## ⚠️ Known Limitations

1. **Token Limits**: Large PRs may exceed LLM token limits. The system truncates content but may miss some issues.

2. **API Rate Limits**: GitHub and LLM APIs have rate limits. The system includes basic error handling but may fail on high-volume usage.

3. **Language Support**: While the system works with any language, specialized analysis is optimized for Python and JavaScript/TypeScript.

4. **Comment Positioning**: GitHub's API sometimes has issues with comment positioning on certain diff formats. The system falls back to issue comments when inline comments fail.

5. **Cost**: LLM API calls incur costs. Monitor usage, especially with large repositories.

6. **Context Understanding**: AI may not fully understand complex business logic or domain-specific requirements.

7. **False Positives**: Static analysis may flag intentional patterns (e.g., test code, examples).

## 🚀 Future Improvements

### Short Term
- [ ] Add support for GitLab and Bitbucket
- [ ] Implement caching to reduce redundant API calls
- [ ] Add support for incremental reviews (only changed lines)
- [ ] Improve comment deduplication logic
- [ ] Add metrics and analytics dashboard

### Medium Term
- [ ] Support for local LLM models (Ollama, LLaMA)
- [ ] Multi-language documentation generation
- [ ] Integration with SAST tools (SonarQube, Snyk)
- [ ] Custom rule marketplace/sharing
- [ ] Webhook-based deployment option

### Long Term
- [ ] Learning from accepted/rejected suggestions
- [ ] Team-specific style guide training
- [ ] Automated fix application (auto-commit)
- [ ] IDE plugin for pre-commit review
- [ ] Multi-repository analysis and insights

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact: yogesh@example.com

## 🙏 Acknowledgments

- OpenAI for GPT models
- Anthropic for Claude
- GitHub for the excellent API
- The open-source community

---

**Built with ❤️ using Python, AI, and modern DevOps practices**
