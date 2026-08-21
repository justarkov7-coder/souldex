---
name: adaptive-model-router
description: Route non-trivial repository exploration, implementation, debugging, tests, reviews, and orchestration to the least costly Codex agent tier likely to succeed. Use for agent/model escalation decisions, bounded parallel work, or when deciding whether to remain single-agent.
---

# Adaptive Model Router

Keep one main writer on Terra/Medium. Do not delegate a short, coherent task without a real isolation or parallelism benefit.

| Work | Agent and tier | Use when |
| --- | --- | --- |
| Narrow, read-only lookup | `scout` · Luna/Low | A precise repository question can be answered independently. |
| Deterministic mechanical operation | `mechanic` · Luna/Low | Inputs and acceptance criteria are explicit. |
| Implementation, debugging, refactor | `engineer` · Terra/Medium | The task needs normal development judgment. |
| Deep read-only diagnosis/review | `reviewer` · Terra/High | The risk or ambiguity needs an independent technical assessment. |
| Critical or unresolved complexity | `expert` · Sol/High | Security, integrity, concurrency, migration, architecture ambiguity, or a reasoned Terra failure requires it. |

Do not use Sol merely for reassurance. Do not use Luna for ambiguity or a material design decision.

- Delegate only independent work; normally use at most two or three agents and never more than four.
- Give each agent a bounded objective, ownership, likely files, constraints, and success criterion.
- Never let two agents edit the same files. Serialize code changes; use isolated Git worktrees only when parallel writes materially pay off.
- Start with the lowest tier that fits. Escalate a failed scout/mechanic to an engineer; escalate to expert only after a reasoned failure or for clearly critical work.
- After a modification, run relevant checks. For a substantial change, use `$claude-review-gate` before completion.

Before delegation, emit: `ROUTING — <agent> · <tier> · <bounded objective>`.

At handoff, report configured tiers, validation, and escalation. Do not claim the provider actually used a model unless execution metadata confirms it.
