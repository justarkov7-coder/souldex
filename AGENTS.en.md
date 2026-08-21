# Codex + Claude workflow

<p align="center">
  <a href="AGENTS.md"><kbd>🇫🇷 Français</kbd></a>
  &nbsp;
  <a href="AGENTS.en.md"><kbd>🇬🇧 English</kbd></a>
</p>

For every non-trivial request, start with this compact triage:

```text
CHALLENGE — SKIP | READY | READY UNDER ASSUMPTIONS | NEEDS CLARIFICATION
Outcome: …
Recommended path: …
Assumptions: …
Validation: …
```

- `SKIP`: a mechanical, low-risk change with obvious validation.
- `EXPLORE`: read repository material first when it can resolve uncertainty.
- `DECIDE`: ask only when a decision materially changes the result or required authority.
- Keep one writing agent by default. Delegate research or review only when isolation has a real benefit.
- After a substantial change, run appropriate checks and then the independent review: `ai-review-loop --repo . --review-only --report-only`.
- A Claude `FAIL` is evidence to verify, never a blind instruction. Fix only valid findings, test, and run a focused review again.
- Do not declare completion before reading a terminal verdict. Never push, publish, or deploy without explicit instruction.
