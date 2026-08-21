#!/usr/bin/env python3
"""Create a bounded, secret-aware review packet from a Git worktree."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

EXCLUDED = {".git", "node_modules", ".next", "dist", "coverage", "playwright-report", "test-results"}
RISK_WORDS = ("auth", "security", "permission", "migration", "schema", "store", "repository", "persistence", "sql", "api/")


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True, stderr=subprocess.DEVNULL)


def allowed(name: str) -> bool:
    path = Path(name)
    return not any(part in EXCLUDED for part in path.parts) and not path.name.startswith(".env")


def digest(path: Path) -> str:
    if not path.is_file() or path.is_symlink():
        return "<missing>"
    value = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def changed(repo: Path, base: str) -> list[str]:
    names: set[str] = set()
    has_head = subprocess.run(["git", "-C", str(repo), "rev-parse", "--verify", "--quiet", "HEAD"], stdout=subprocess.DEVNULL).returncode == 0
    diffs = [("diff", "--name-only", f"{base}...HEAD")]
    diffs += [("diff", "--name-only", "HEAD")] if has_head else [("diff", "--name-only"), ("diff", "--name-only", "--cached")]
    for arguments in (*diffs, ("ls-files", "--others", "--exclude-standard")):
        try:
            names.update(line for line in git(repo, *arguments).splitlines() if line)
        except subprocess.CalledProcessError:
            pass
    return sorted(name for name in names if allowed(name))


def patch(repo: Path, base: str, names: list[str]) -> str:
    result: list[str] = []
    has_head = subprocess.run(["git", "-C", str(repo), "rev-parse", "--verify", "--quiet", "HEAD"], stdout=subprocess.DEVNULL).returncode == 0
    diffs = [("diff", "--no-ext-diff", "--unified=40", f"{base}...HEAD", "--", *names)]
    diffs += [("diff", "--no-ext-diff", "--unified=40", "HEAD", "--", *names)] if has_head else [("diff", "--no-ext-diff", "--unified=40", "--", *names), ("diff", "--no-ext-diff", "--cached", "--unified=40", "--", *names)]
    for arguments in diffs:
        try:
            output = git(repo, *arguments)
            if output:
                result.append(output)
        except subprocess.CalledProcessError:
            pass
    untracked = set(git(repo, "ls-files", "--others", "--exclude-standard").splitlines())
    for name in names:
        file = repo / name
        if name in untracked and file.is_file() and not file.is_symlink():
            lines = file.read_text(errors="replace").splitlines()
            result.append(f"diff --git a/{name} b/{name}\nnew file mode 100644\n--- /dev/null\n+++ b/{name}\n" + "\n".join(f"+{line}" for line in lines))
    return "\n".join(result) or "# No source files in review scope.\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--base", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--mode", choices=("auto", "fast", "deep"), default="auto")
    parser.add_argument("--task", required=True)
    args = parser.parse_args()
    repo, output = Path(args.repo), Path(args.out)
    names = changed(repo, args.base)
    diff = patch(repo, args.base, names)
    lines = sum(1 for line in diff.splitlines() if line.startswith(("+", "-")) and not line.startswith(("+++", "---")))
    source = [name for name in names if not name.endswith((".md", ".txt"))]
    risky = any(word in name.lower() for name in source for word in RISK_WORDS)
    mode = args.mode if args.mode != "auto" else ("deep" if risky or len(source) > 12 or lines > 1200 else "fast")
    limit = 24_000 if mode == "fast" else 180_000
    truncated = len(diff) > limit
    (output / "review-diff.patch").write_text(diff[:limit] + ("\n# PATCH TRUNCATED\n" if truncated else ""))
    scope = {"mode": mode, "base_ref": args.base, "task": args.task, "files": names, "source_files": source, "risk_detected": risky, "changed_lines": lines, "diff_truncated": truncated, "snapshot": {name: digest(repo / name) for name in names}}
    (output / "scope.json").write_text(json.dumps(scope, indent=2) + "\n")
    file_list = "\n".join(f"- `{name}`" for name in names) or "- none"
    (output / "review-packet.md").write_text(f"# Independent review packet\n\nMode: {mode}\nTask: {args.task}\nBase: {args.base}\n\n## Files in scope\n{file_list}\n\n## Rules\n- Findings must concern a changed file or its direct contract.\n- Do not report style-only issues.\n- Do not inspect files outside this packet without a concrete boundary reason.\n")


if __name__ == "__main__":
    main()
