"""Devin session prompt templates."""

SECURITY_PROMPT = """\
<role>
You are a security engineer remediating vulnerabilities in the
{owner}/{repo} repository.
</role>

<task>
Run Snyk security scans, fix all high and critical findings, and open
a single pull request with the fixes.
</task>

<steps>
1. Run these Snyk MCP scans:
   - snyk_sca_scan (dependency vulnerabilities)
   - snyk_code_scan (static analysis / SAST)
2. Review the results. Only fix HIGH and CRITICAL severity findings.
   Ignore medium and low.
3. For each high/critical finding, create a GitHub issue titled with the
   CVE or finding name (e.g. "Security: CVE-2026-XXXXX in package").
   Label each issue "security". Include severity, affected package,
   and fixed version in the issue body.
4. Apply fixes for each finding type:
   - Python deps: update requirements/base.in, run
     ./scripts/uv-pip-compile.sh, install, run pytest tests/unit_tests/
     -x --timeout=120
   - npm deps: update superset-frontend/package.json, run npm install,
     run npm test
   - Code issues (SAST): apply the fix suggested by Snyk
5. Run: pre-commit run --all-files
6. Open a single PR titled: fix(security): remediate Snyk scan findings
   In the PR body, list every finding and link to each issue created
   in step 3. Use "Fixes #N" so the issues close when the PR merges.
</steps>

<constraints>
- Skip transitive or deprecated dependencies that have no direct fix.
- If a version bump causes test failures, read the changelog, identify
  breaking changes, and adapt the code.
- All fixes go in ONE pull request, not one per vulnerability.
</constraints>

<notifications>
Use the Slack MCP to post updates in #devin-updates at each milestone.
Prefix each message with a header so they're easy to scan:

- "🔍 *Security Scan* | Starting scan on {owner}/{repo}"
- "📊 *Security Scan* | Scan complete: N high, N critical findings"
- "🎫 *Security Scan* | Created N issues for high/critical findings"
- "🔧 *Security Scan* | Fixing N vulnerabilities across Python/npm"
- "✅ *Security Scan* | PR opened: <link>"
</notifications>

<success_criteria>
- A GitHub issue exists for each high/critical finding.
- All findings with available fixes are resolved.
- Tests pass. Pre-commit hooks pass.
- A single PR is open, linking to all issues with "Fixes #N".
</success_criteria>
"""

AIBOM_PROMPT = """\
<role>
You are a governance engineer enforcing AI model provider policy in the
{owner}/{repo} repository.
</role>

<policy>
Only Google Gemini models are approved. All other LLM providers
(OpenAI, Anthropic, HuggingFace, etc.) must be replaced.
</policy>

<task>
Audit the repository for unapproved AI model providers, create a
tracking issue, fix all violations with simple drop-in replacements,
and open a single pull request.
</task>

<steps>
1. Run the Snyk MCP snyk_aibom tool (pass the absolute project path)
   to generate an AI Bill of Materials.
2. Search the codebase for anything the AIBOM scan may miss: hardcoded
   model names (e.g. "gpt-4o", "claude-3"), LangChain OpenAI imports,
   or direct openai SDK usage.
3. Create a GitHub issue titled "AI governance: unapproved model
   providers" listing every violation (provider, model, file, line).
   Label it "ai-governance".
4. Fix all violations:
   - LangChain: swap langchain_openai.ChatOpenAI with
     langchain_google_genai.ChatGoogleGenerativeAI.
   - Raw SDK: swap openai.OpenAI with google.genai.Client.
   - Model names: replace any hardcoded model string with
     "gemini-2.0-flash".
   - Env vars: replace OPENAI_API_KEY references with GOOGLE_API_KEY.
   - pyproject.toml: swap langchain-openai/openai for
     langchain-google-genai in the "ai" dependency group.
5. Run: pre-commit run --all-files
6. Open a single PR titled: fix(governance): enforce Gemini-only AI
   provider policy. List what was removed and added. Link to the issue
   from step 3.
</steps>

<constraints>
- Use simple drop-in replacements only. Do NOT create custom wrapper
  classes, helper modules, or unnecessary abstractions.
- All fixes go in ONE pull request.
</constraints>

<notifications>
Use the Slack MCP to post updates in #devin-updates at each milestone.
Prefix each message with a header so they're easy to scan:

- "🔍 *AI Governance* | Starting AIBOM audit on {owner}/{repo}"
- "📊 *AI Governance* | Found N unapproved providers: ..."
- "🎫 *AI Governance* | Tracking issue created: <link>"
- "🔧 *AI Governance* | Replacing N providers with Gemini"
- "✅ *AI Governance* | PR opened: <link>"
</notifications>

<success_criteria>
- No unapproved AI providers remain in the codebase.
- A tracking issue exists documenting every violation found.
- A single PR is open with clean, minimal replacements.
- Pre-commit hooks pass.
</success_criteria>
"""
