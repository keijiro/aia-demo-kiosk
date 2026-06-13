"""Shared helper: point the anthropic SDK at Unity's LiteLLM via Keychain.

Mirrors x-watcher/.claude/skills/x-unity-report/analyze_tweets.py: if
ANTHROPIC_BASE_URL / ANTHROPIC_AUTH_TOKEN are unset, populate them from the
macOS Keychain items LITELLM_BASE_URL / LITELLM_AUTH_TOKEN.
"""
import os, sys, subprocess


def populate_anthropic_env_from_keychain() -> None:
    mapping = {
        "ANTHROPIC_BASE_URL": "LITELLM_BASE_URL",
        "ANTHROPIC_AUTH_TOKEN": "LITELLM_AUTH_TOKEN",
    }
    user = os.environ.get("USER", "")
    for env_key, kc_key in mapping.items():
        if os.environ.get(env_key):
            continue
        for cmd in (
            ["security", "find-generic-password", "-a", user, "-s", kc_key, "-w"],
            ["security", "find-generic-password", "-s", kc_key, "-w"],
        ):
            r = subprocess.run(cmd, capture_output=True, text=True)
            if r.returncode == 0 and r.stdout.strip():
                os.environ[env_key] = r.stdout.strip()
                break
        else:
            sys.exit(f"Missing Keychain item: {kc_key}")
