# Next Steps

## 1. Shift Left: Run on Every Pull Request

Today Guardian runs on a weekly schedule. The highest-impact change is moving it into the CI/CD pipeline so every PR is scanned before it merges. A GitHub Action triggered on `pull_request` would dispatch a Devin session scoped to the diff -- catching vulnerabilities and unapproved AI providers before they reach main, not after.

**Business value**: Zero security debt accumulates. New vulnerabilities are blocked at the gate, not triaged from a backlog weeks later.

## 2. Multi-Repo Coverage

The orchestrator currently targets a single repository. Extending it to loop over a list of repositories (or discovering them via the GitHub API by team/topic) means one Guardian instance protects the entire engineering org.

**Business value**: Consistent security and governance posture across every service, not just the ones that get attention.

## 3. Policy as Config

The AI governance policy ("only Gemini") is embedded in the Devin prompt. Moving it to a config file (e.g. `policy.yml`) lets engineering leadership update approved providers, severity thresholds, or scan types without touching code. Non-engineers can own the policy.

**Business value**: Governance becomes a business decision, not a code change. Auditors can review the policy file directly.

## 4. Metrics and Reporting

Slack notifications give real-time visibility, but leadership needs trends. Pushing structured data (findings count, fix rate, mean time to remediate) to a dashboard tool like Datadog or Grafana would answer: "Are we getting more secure over time?"

**Business value**: Executive-ready reporting that ties engineering automation to measurable risk reduction.

## 5. Go Native: Playbooks, Knowledge, and Scheduled Sessions

The current orchestrator is a thin Python script that dispatches sessions with prompt templates. Devin's platform has native features that replace most of this scaffolding:

- **Playbooks** -- Convert the security and governance prompts into versioned, org-level playbooks that any engineer can trigger with a macro (e.g. `!security-scan`). No orchestrator needed.
- **Knowledge Base** -- Persist context across sessions: approved AI providers, internal tooling conventions, repos to skip. Devin recalls relevant knowledge automatically instead of needing everything in the prompt.
- **Native Scheduling** -- Devin's scheduling API supports cron expressions with timezone support. Replace the GitHub Action and Docker container with a single API call -- no infrastructure to maintain.

**Business value**: Eliminates the orchestrator entirely. Security and governance become a platform capability that scales with the team, not a bespoke script that one person maintains.
