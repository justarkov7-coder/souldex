# Architecture and protocol

[🇫🇷 Français](i18n/fr/workflow.md) · [🇬🇧 English](workflow.md)

## 1. Challenge before action

Every non-trivial request is classified before work starts:

- `SKIP` for a small, reversible change with clear validation;
- `EXPLORE` when reading repository material can resolve uncertainty;
- `DECIDE` when a product, security, cost, or authority choice is required.

The challenge records the expected outcome, assumptions, and validation. It does not replace code analysis or tests.

## 2. Agent and inference routing

Versioned skills live in `.codex/skills/`: `$intent-challenger`, `$adaptive-model-router`, and `$claude-review-gate`. They are the workflow orchestrator; no script replaces or downloads a model.

The router keeps Terra/Medium as the primary writer. It reserves Luna/Low for targeted research or mechanical work, Terra/High for difficult diagnosis and review, and Sol/High for critical work (security, integrity, concurrency, migration, or architecture ambiguity). It stays single-agent when parallelism has no real benefit, limits delegation to four agents, and forbids two writers on the same files.

## 3. One writer

Codex is the only process allowed to modify the worktree. Claude is never granted editing, write, web, or MCP access. This separation avoids concurrent writes and makes the owner of each correction explicit.

## 4. Bounded review packet

`build-review-packet.py` collects modified and untracked files, excludes heavy directories and `.env` files, then creates:

- `review-packet.md`, the scope and rules;
- `review-diff.patch`, a diff capped at 24k characters in fast mode and 180k in deep mode;
- `scope.json`, the mode, files, risk heuristic, and SHA-256 fingerprint of each file.

Deep mode is selected automatically when a filename indicates a sensitive boundary, more than 12 source files change, or the diff exceeds 1,200 lines. These heuristics are guardrails, not a complete security classification.

## 5. Independent verdict

Claude must return only the JSON defined in `schemas/findings.schema.json`. The runner rejects incomplete formats, extra fields, and contradictory verdicts. It also checks that the Git worktree did not change during review.

## 6. Correction loop

A `FAIL` stops the gate with exit code 3. The implementer:

1. verifies the evidence;
2. discards false positives;
3. fixes the root cause of valid findings;
4. runs targeted checks;
5. runs a review again.

The runner never automatically fixes a `FAIL`. This is deliberate: a review conclusion is not an executable instruction.
