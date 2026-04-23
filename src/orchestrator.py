"""Dispatch Devin sessions for security scanning and AI governance."""

from __future__ import annotations

import logging
import sys

import requests

from src import config, prompts

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("guardian")


def _devin_session(prompt: str, tags: list[str]) -> dict:
    """Create a Devin session via the v3 API."""
    url = f"{config.DEVIN_API_BASE}/organizations/{config.DEVIN_ORG_ID}/sessions"
    headers = {"Authorization": f"Bearer {config.DEVIN_API_KEY}", "Content-Type": "application/json"}
    payload = {"prompt": prompt, "repos": [config.TARGET_REPO_URL], "tags": tags}
    log.info("Dispatching Devin session %s", tags)
    resp = requests.post(url, json=payload, headers=headers, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    log.info("Session created: %s (%s)", data.get("session_id", "?"), data.get("url", ""))
    return data


def main() -> None:
    if not config.DEVIN_API_KEY or not config.DEVIN_ORG_ID:
        sys.exit("DEVIN_API_KEY and DEVIN_ORG_ID are required.")

    log.info("=== Devin Guardian ===")
    owner, repo = config.TARGET_REPO.split("/")

    _devin_session(
        prompts.SECURITY_PROMPT.format(owner=owner, repo=repo),
        ["snyk-remediation", "security"],
    )

    _devin_session(
        prompts.AIBOM_PROMPT.format(owner=owner, repo=repo),
        ["ai-governance", "aibom"],
    )

    log.info("=== Done ===")


if __name__ == "__main__":
    main()
