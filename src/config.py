"""Environment variables and constants."""

import os

DEVIN_API_KEY = os.environ.get("DEVIN_API_KEY", "") or os.environ.get("DEVIN_TOKEN", "")
DEVIN_ORG_ID = os.environ.get("DEVIN_ORG_ID", "")

TARGET_REPO = os.environ.get("TARGET_REPO", "oarmstrong95/superset")
TARGET_REPO_URL = os.environ.get("TARGET_REPO_URL", f"https://github.com/{TARGET_REPO}")

DEVIN_API_BASE = "https://api.devin.ai/v3"

SECURITY_PLAYBOOK_ID = os.environ.get("SECURITY_PLAYBOOK_ID", "")
GOVERNANCE_PLAYBOOK_ID = os.environ.get("GOVERNANCE_PLAYBOOK_ID", "")
SECURITY_FIX_PLAYBOOK_ID = os.environ.get("SECURITY_FIX_PLAYBOOK_ID", "")
