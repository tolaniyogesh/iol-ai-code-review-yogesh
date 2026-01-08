# Quick Start Guide

Get your AI Code Review Assistant up and running in 5 minutes!

## Prerequisites Checklist

- [ ] Python 3.11 or higher installed
- [ ] GitHub account with repository access
- [ ] API key from one of: Google Gemini (FREE), OpenAI, Anthropic, or Azure OpenAI
- [ ] Git installed

## Step 1: Get Your API Key (2 minutes)

### Option A: Google Gemini (FREE - Recommended) ⭐
1. Visit https://aistudio.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Copy the key (starts with `AIza...`)
5. **Cost**: FREE! No credit card required
6. **Models Available:**
   - Gemini 1.5 Flash: 1500 requests/day (fast, great quality)
   - Gemini 1.5 Pro: 50 requests/day (best quality)
7. **Perfect for:** All team sizes, production use

### Option B: OpenAI
1. Visit https://platform.openai.com/api-keys
2. Sign in or create an account
3. Add payment method (required)
4. Click "Create new secret key"
5. Copy the key (starts with `sk-`)
6. **Cost**: ~$0.01-$0.30 per PR review

### Option C: Anthropic
1. Visit https://console.anthropic.com/
2. Sign in or create an account
3. Add payment method (required)
4. Navigate to API Keys
5. Create a new key
6. Copy the key (starts with `sk-ant-`)

### Option D: Azure OpenAI
1. Create Azure OpenAI resource in Azure Portal
2. Deploy a model (e.g., gpt-4)
3. Get API key and endpoint from Keys and Endpoint section

## Step 2: Setup GitHub Repository (2 minutes)

### Add GitHub Secrets

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add these secrets:

**For Google Gemini (FREE - Recommended):**
```
Name: GEMINI_API_KEY
Value: AIza...your-actual-key-here

Name: LLM_PROVIDER
Value: gemini

Name: LLM_MODEL
Value: gemini-1.5-flash
```

**For OpenAI:**
```
Name: OPENAI_API_KEY
Value: sk-your-actual-key-here
```

**For Anthropic:**
```
Name: ANTHROPIC_API_KEY
Value: sk-ant-your-actual-key-here

Name: LLM_PROVIDER
Value: anthropic
```

**For Azure OpenAI:**
```
Name: AZURE_OPENAI_API_KEY
Value: your-azure-key

Name: AZURE_OPENAI_ENDPOINT
Value: https://your-resource.openai.azure.com/

Name: AZURE_OPENAI_DEPLOYMENT
Value: your-deployment-name

Name: LLM_PROVIDER
Value: azure
```

## Step 3: Add Workflow File (1 minute)

### Option A: If this is your project repository

The workflow file is already at `.github/workflows/ai-review.yml` - you're all set!

### Option B: If adding to another repository

1. Copy the workflow file:
```bash
mkdir -p .github/workflows
cp path/to/iol-ai-code-review-yogesh/.github/workflows/ai-review.yml .github/workflows/
```

2. Copy the configuration file:
```bash
cp path/to/iol-ai-code-review-yogesh/.ai-review.yaml .
```

3. Copy the source code:
```bash
cp -r path/to/iol-ai-code-review-yogesh/src .
cp path/to/iol-ai-code-review-yogesh/requirements.txt .
```

4. Commit and push:
```bash
git add .github/workflows/ai-review.yml .ai-review.yaml src/ requirements.txt
git commit -m "Add AI code review assistant"
git push
```

## Step 4: Test It! (30 seconds)

### Create a Test PR

1. Create a new branch:
```bash
git checkout -b test-ai-review
```

2. Create a test file with intentional issues:
```bash
cat > test_security.py << 'EOF'
import sqlite3

# Hardcoded credentials - should be flagged
API_KEY = "sk-1234567890abcdef"
PASSWORD = "admin123"

def get_user(user_id):
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    
    # SQL injection vulnerability - should be flagged
    query = "SELECT * FROM users WHERE id = " + user_id
    cursor.execute(query)
    
    return cursor.fetchone()

# Using eval - should be flagged
def process_input(data):
    return eval(data)

if __name__ == "__main__":
    print("Test file")
EOF
```

3. Commit and push:
```bash
git add test_security.py
git commit -m "Test: Add file with security issues"
git push origin test-ai-review
```

4. Create a Pull Request on GitHub

5. Watch the magic happen! 🎉

Within 1-2 minutes, you should see:
- ✅ GitHub Actions workflow running
- 🤖 AI comments on your PR
- 📊 Review summary

## Expected Output

You should see comments like:

```
🔴 Critical Security

Hardcoded API key detected. Use environment variables instead.

Suggested Fix:
API_KEY = os.getenv('API_KEY')
```

```
🔴 Critical Security

SQL injection vulnerability: User input is directly concatenated into SQL query

Suggested Fix:
Use parameterized queries: cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
```

## Troubleshooting

### "Workflow not running"
- Check that secrets are added correctly
- Verify workflow file is in `.github/workflows/`
- Check workflow permissions in Settings → Actions

### "Authentication failed"
- Verify API key is correct (no extra spaces)
- Check API key hasn't expired
- Ensure you have credits/quota available

### "No comments posted"
- Check GitHub Actions logs for errors
- Verify `GITHUB_TOKEN` has write permissions
- Check if files match ignore patterns in `.ai-review.yaml`

### "Rate limit exceeded"
- Wait for rate limit to reset
- Reduce `max_comments_per_file` in config
- Use a different API key

## Customization

### Adjust Review Strictness

Edit `.ai-review.yaml`:

```yaml
# Strict mode - block PRs with critical issues
severity_config:
  block_pr_on_critical: true
  block_pr_on_warning: false
  min_severity_to_comment: "warning"

# Lenient mode - only suggestions
severity_config:
  block_pr_on_critical: false
  block_pr_on_warning: false
  min_severity_to_comment: "suggestion"
```

### Focus on Specific Areas

```yaml
focus_areas:
  code_quality: true
  security: true      # Enable security checks
  performance: false  # Disable performance checks
  best_practices: true
  documentation: false
```

### Ignore Specific Files

```yaml
ignore_patterns:
  - "*.md"
  - "*.txt"
  - "tests/**"
  - "vendor/**"
  - "node_modules/**"
  - "dist/**"
```

## Next Steps

1. ✅ Test with sample PR (done!)
2. 📝 Customize `.ai-review.yaml` for your project
3. 🚀 Enable for all PRs to main/develop branches
4. 📊 Monitor feedback and adjust configuration
5. 🎯 Add custom rules specific to your codebase

## Cost Management

### Estimate Your Costs

**Small team (10 PRs/day):**
- **Google Gemini Flash: $0/day** ✅ FREE (up to 1500 requests/day)
- **Google Gemini Pro: $0/day** ✅ FREE (up to 50 requests/day)
- OpenAI GPT-4: ~$3-5/day
- OpenAI GPT-3.5: ~$0.30-0.50/day
- Anthropic Claude: ~$2-4/day

**Tips to reduce costs:**
1. Use Gemini (FREE) or GPT-3.5 instead of GPT-4:
```bash
# For FREE option
LLM_PROVIDER=gemini
LLM_MODEL=gemini-1.5-flash

# For cheaper paid option
LLM_PROVIDER=openai
LLM_MODEL=gpt-3.5-turbo
```

2. Limit comments:
```yaml
review_settings:
  max_comments_per_file: 5
  max_total_comments: 25
```

3. Ignore non-critical files:
```yaml
ignore_patterns:
  - "tests/**"
  - "docs/**"
  - "*.md"
```

## Local Testing (Optional)

Test locally before pushing:

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your credentials
nano .env

# Install dependencies
pip install -r requirements.txt

# Run on existing PR
export GITHUB_PR_NUMBER=123
python -m src.main
```

## Getting Help

- 📖 Read [README.md](README.md) for detailed documentation
- 🔒 Check [SECURITY.md](SECURITY.md) for security best practices
- 🐛 Report issues on GitHub
- 💬 Ask questions in Discussions

## Success! 🎉

You now have an AI-powered code review assistant running on your repository!

Every new PR will automatically get reviewed with:
- ✅ Security vulnerability detection
- ✅ Performance issue identification
- ✅ Code quality suggestions
- ✅ Best practice recommendations
- ✅ Documentation checks

### Security Features

Your repository now includes:
- 🔒 Automated security scanning (see `.github/workflows/security-scan.yml`)
- 🛡️ Dependency vulnerability checks
- 🔍 Secret scanning with TruffleHog
- 📊 Code quality analysis with Bandit, Pylint, Flake8

### Model Options

**For best quality:** Use Gemini 1.5 Pro (FREE, 50 requests/day)
```bash
LLM_MODEL=gemini-1.5-pro
```

**For high volume:** Use Gemini 1.5 Flash (FREE, 1500 requests/day)
```bash
LLM_MODEL=gemini-1.5-flash
```

**Happy coding!** 🚀
