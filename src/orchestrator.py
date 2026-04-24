"""Dispatch Devin sessions using playbooks and batch mode."""

from __future__ import annotations

import logging
import sys

import requests

from src import config, prompts

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("guardian")

def _headers() -> dict:
    return {"Authorization": f"Bearer {config.DEVIN_API_KEY}", "Content-Type": "application/json"}


def _playbook_url() -> str:
    return f"{config.DEVIN_API_BASE}/organizations/{config.DEVIN_ORG_ID}/playbooks"


def _list_playbooks() -> list[dict]:
    resp = requests.get(_playbook_url(), headers=_headers(), timeout=30)
    resp.raise_for_status()
    return resp.json().get("items", [])


def _ensure_playbook(title: str, body: str, macro: str) -> str:
    """Create or update a playbook. Returns the playbook_id."""
    existing = [p for p in _list_playbooks() if p.get("macro") == macro]
    if existing:
        pb = existing[0]
        if pb.get("body") != body:
            url = f"{_playbook_url()}/{pb['playbook_id']}"
            requests.put(url, json={"title": title, "body": body, "macro": macro},
                         headers=_headers(), timeout=30).raise_for_status()
            log.info("Updated playbook %s (%s)", macro, pb["playbook_id"])
        else:
            log.info("Playbook %s up to date (%s)", macro, pb["playbook_id"])
        return pb["playbook_id"]

    resp = requests.post(_playbook_url(), json={"title": title, "body": body, "macro": macro},
                         headers=_headers(), timeout=30)
    resp.raise_for_status()
    pid = resp.json()["playbook_id"]
    log.info("Created playbook %s (%s)", macro, pid)
    return pid


def _devin_session(
    prompt: str,
    tags: list[str],
    playbook_id: str | None = None,
    advanced_mode: str | None = None,
    child_playbook_id: str | None = None,
) -> dict:
    """Create a Devin session via the v3 API."""
    url = f"{config.DEVIN_API_BASE}/organizations/{config.DEVIN_ORG_ID}/sessions"
    payload: dict = {"prompt": prompt, "repos": [config.TARGET_REPO_URL], "tags": tags}
    if playbook_id:
        payload["playbook_id"] = playbook_id
    if advanced_mode:
        payload["advanced_mode"] = advanced_mode
    if child_playbook_id:
        payload["child_playbook_id"] = child_playbook_id

    log.info("Dispatching Devin session %s (mode=%s)", tags, advanced_mode or "standard")
    resp = requests.post(url, json=payload, headers=_headers(), timeout=30)
    resp.raise_for_status()
    data = resp.json()
    log.info("Session created: %s (%s)", data.get("session_id", "?"), data.get("url", ""))
    return data


def main() -> None:
    if not config.DEVIN_API_KEY or not config.DEVIN_ORG_ID:
        sys.exit("DEVIN_API_KEY and DEVIN_ORG_ID are required.")

    log.info("=== Devin Guardian ===")
    owner, repo = config.TARGET_REPO.split("/")

    log.info("Ensuring playbooks exist ...")
    sec_id = _ensure_playbook(
        "Guardian: Security Scan",
        prompts.SECURITY_PROMPT.format(owner=owner, repo=repo),
        "!guardian-security",
    )
    fix_id = _ensure_playbook(
        "Guardian: Security Fix (child)",
        prompts.SECURITY_FIX_PROMPT.format(owner=owner, repo=repo),
        "!guardian-security-fix",
    )
    gov_id = _ensure_playbook(
        "Guardian: AI Governance",
        prompts.AIBOM_PROMPT.format(owner=owner, repo=repo),
        "!guardian-governance",
    )

    _devin_session(
        prompts.SECURITY_PROMPT.format(owner=owner, repo=repo),
        ["snyk-remediation", "security"],
        playbook_id=sec_id,
        advanced_mode="batch",
        child_playbook_id=fix_id,
    )

    _devin_session(
        prompts.AIBOM_PROMPT.format(owner=owner, repo=repo),
        ["ai-governance", "aibom"],
        playbook_id=gov_id,
    )

    log.info("=== Done ===")


if __name__ == "__main__":
    main()
