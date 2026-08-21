# Security model

[🇫🇷 Français](security.md) · [🇬🇧 English](security.en.md)

## Data and publication

This repository must not contain review logs, `.env` files, tokens, or personal Claude/Codex settings. User paths are resolved through `$HOME` at runtime, and package resources are resolved relative to the scripts.

Before creating a fork or contribution, run:

```bash
git grep -nE '(/Users/|/home/|API[_-]?KEY|AUTH[_-]?TOKEN|GITHUB_TOKEN|BEGIN (RSA|OPENSSH))' || true
```

Every result must either be removed or be a documented variable name with no value. Never add artifacts from `~/.local/state/codex-claude-review`.

## Required Claude configuration

Apply the principles from `config/claude-settings.example.json` to your Claude configuration: sandbox enabled, failure when unavailable, write denied, and cloud or registry credentials denied. Adjust temporary paths for your operating system. Never copy a personal settings file into this repository.

The runner also passes `--disallowedTools` to block write tools, web access, interactive questions, and MCP. This defense in depth does not replace sandbox configuration: `--dry-run` only checks local CLIs and bundled resources, so also confirm that your Claude configuration enables the sandbox.

## Explicit boundaries

- Claude receives the review prompt, packet, and diff. Do not use it on code or data your policy forbids sending to the provider.
- Deep mode may read files needed for analysis inside the Claude sandbox. Fast mode uses no tools.
- CI checks and human review remain necessary for critical changes.
