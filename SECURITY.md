# Security Policy

## Reporting Security Vulnerabilities

If you discover a security vulnerability in this project, please report it responsibly:

1. **DO NOT** open a public GitHub issue
2. Email the maintainers directly (or use GitHub Security Advisories)
3. Provide detailed information about the vulnerability
4. Allow reasonable time for a fix before public disclosure

## Security Best Practices

### For Users

#### 1. API Keys & Secrets Management

**✅ DO:**
- Store API keys in environment variables or GitHub Secrets
- Use `.env` file locally (already in `.gitignore`)
- Rotate API keys regularly
- Use separate API keys for development and production

**❌ DON'T:**
- Hardcode API keys in source code
- Commit `.env` files to version control
- Share API keys in public channels
- Use production keys in development

#### 2. GitHub Token Permissions

**Minimum Required Permissions:**
```yaml
permissions:
  contents: read        # Read repository contents
  pull-requests: write  # Post review comments
```

**✅ DO:**
- Use fine-grained personal access tokens
- Limit token scope to specific repositories
- Set token expiration dates
- Revoke unused tokens

**❌ DON'T:**
- Use classic tokens with full repo access
- Share tokens between projects
- Use tokens without expiration

#### 3. Environment Variables

**Required (Sensitive):**
```bash
GITHUB_TOKEN=ghp_xxxxx          # Keep secret
OPENAI_API_KEY=sk-xxxxx         # Keep secret
ANTHROPIC_API_KEY=sk-ant-xxxxx  # Keep secret
GEMINI_API_KEY=AIza-xxxxx       # Keep secret
```

**Configuration (Non-Sensitive):**
```bash
LLM_PROVIDER=gemini
LLM_MODEL=gemini-1.5-flash
GITHUB_REPOSITORY=owner/repo
```

#### 4. GitHub Actions Security

**✅ DO:**
- Use GitHub Secrets for sensitive data
- Pin action versions (e.g., `@v4` not `@main`)
- Review third-party actions before use
- Enable branch protection rules

**❌ DON'T:**
- Echo secrets in workflow logs
- Use `pull_request_target` without validation
- Run untrusted code in workflows

### For Contributors

#### 1. Code Security

**✅ DO:**
- Validate all user inputs
- Use parameterized queries (if using databases)
- Sanitize file paths
- Use `yaml.safe_load()` not `yaml.load()`
- Handle exceptions properly
- Log errors without sensitive data

**❌ DON'T:**
- Use `eval()` or `exec()`
- Use `subprocess` with `shell=True`
- Trust user input without validation
- Log API keys or secrets
- Use pickle for untrusted data

#### 2. Dependency Management

**✅ DO:**
- Keep dependencies updated
- Run security audits regularly:
  ```bash
  pip install safety
  safety check -r requirements.txt
  ```
- Review dependency licenses
- Pin dependency versions

**❌ DON'T:**
- Use outdated packages with known vulnerabilities
- Install packages from untrusted sources
- Use `pip install` without reviewing packages

#### 3. Code Review

**✅ DO:**
- Review all PRs for security issues
- Run security scans in CI/CD
- Test with malicious inputs
- Verify error handling

**❌ DON'T:**
- Merge without review
- Skip security checks
- Ignore security warnings

## Security Features

### Built-in Security

1. **No Hardcoded Secrets**
   - All sensitive data from environment variables
   - Pydantic Settings for validation

2. **Input Validation**
   - Pydantic models validate all inputs
   - Type checking with MyPy
   - Safe YAML parsing

3. **Secure API Usage**
   - Official SDK libraries (PyGithub, OpenAI, etc.)
   - Proper error handling
   - No command injection vectors

4. **Static Analysis**
   - Detects hardcoded credentials
   - Flags dangerous functions (`eval`, `exec`)
   - Identifies security anti-patterns

### CI/CD Security

Automated security scanning runs on:
- Every push to main/develop
- Every pull request
- Weekly scheduled scans

**Scans Include:**
- Dependency vulnerability scanning (Safety)
- Static security analysis (Bandit)
- Secret scanning (TruffleHog)
- Code quality checks (Pylint, Flake8, MyPy)

## Security Checklist

### Before Deployment

- [ ] All API keys stored in environment variables
- [ ] `.env` file in `.gitignore`
- [ ] GitHub token has minimum required permissions
- [ ] Dependencies updated and scanned
- [ ] Security workflow enabled
- [ ] Branch protection rules configured
- [ ] Secrets configured in GitHub repository settings

### Regular Maintenance

- [ ] Review security scan results weekly
- [ ] Update dependencies monthly
- [ ] Rotate API keys quarterly
- [ ] Review access permissions quarterly
- [ ] Audit logs for suspicious activity

## Known Security Considerations

### 1. LLM API Calls

**Risk:** Code sent to third-party LLM providers

**Mitigation:**
- Use providers with strong privacy policies
- Consider self-hosted models (Gemini free tier)
- Review provider terms of service
- Don't review code with sensitive data

### 2. GitHub API Access

**Risk:** Token compromise could allow unauthorized access

**Mitigation:**
- Use fine-grained tokens
- Limit token scope
- Enable 2FA on GitHub account
- Monitor token usage

### 3. Rate Limiting

**Risk:** Excessive API calls could incur costs or hit limits

**Mitigation:**
- Configure review limits in `.ai-review.yaml`
- Monitor API usage
- Set up billing alerts
- Use free tier providers (Gemini)

## Compliance

### Data Privacy

- Code content sent to LLM providers
- No data stored by this application
- GitHub data accessed via official API
- Logs contain no sensitive information

### GDPR Considerations

- No personal data collected
- No data retention
- No cookies or tracking
- User controls all data flow

## Security Updates

This project follows semantic versioning. Security updates are:
- **Critical:** Patch released within 24 hours
- **High:** Patch released within 1 week
- **Medium:** Patch released in next minor version
- **Low:** Addressed in next major version

## Security Audit History

| Date | Auditor | Findings | Status |
|------|---------|----------|--------|
| 2026-01-07 | Internal | No critical issues | ✅ Resolved |

## Resources

- [GitHub Security Best Practices](https://docs.github.com/en/code-security)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)
- [API Security Checklist](https://github.com/shieldfy/API-Security-Checklist)

## Contact

For security concerns, contact the maintainers through GitHub Security Advisories.

---

**Last Updated:** January 7, 2026  
**Version:** 1.0
