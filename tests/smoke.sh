#!/usr/bin/env bash
set -euo pipefail

project_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
temporary="$(mktemp -d /private/tmp/codex-claude-review-gate.XXXXXX)"
trap 'rm -rf "$temporary"' EXIT
repo="$temporary/repo"; bin="$temporary/bin"
mkdir -p "$repo" "$bin"
git -C "$repo" init -q
git -C "$repo" config user.name test
git -C "$repo" config user.email test@example.invalid
printf 'initial\n' > "$repo/readme.txt"
git -C "$repo" add readme.txt
git -C "$repo" commit -qm initial
printf 'changed\n' > "$repo/readme.txt"
git -C "$repo" add readme.txt
printf 'staged\n' > "$repo/staged.txt"
git -C "$repo" add staged.txt
mkdir "$temporary/packet"
python3 "$project_root/bin/build-review-packet.py" --repo "$repo" --base HEAD --out "$temporary/packet" --mode fast --task smoke
grep -q 'readme.txt' "$temporary/packet/scope.json"
grep -q 'staged.txt' "$temporary/packet/scope.json"
grep -q 'staged.txt' "$temporary/packet/review-diff.patch"

cat > "$bin/claude" <<'EOF'
#!/usr/bin/env bash
printf '%s\n' '{"result":"{\"status\":\"PASS\",\"summary\":\"Mock review passed.\",\"findings\":[]}"}'
EOF
chmod +x "$bin/claude"

AI_REVIEW_CLAUDE_BIN="$bin/claude" AI_REVIEW_STATE_DIR="$temporary/state" \
  bash "$project_root/bin/ai-review-loop" --repo "$repo" --review-only --report-only --fast >/dev/null
find "$temporary/state/runs" -name findings-1.json -type f -print | grep -q findings-1.json
bash "$project_root/bin/ai-review-loop" --help >/dev/null
! grep -RInE '/Users/[[:alnum:]._-]+/|/home/[[:alnum:]._-]+/|BEGIN (RSA|OPENSSH) PRIVATE KEY' "$project_root" --exclude-dir=.git
echo "smoke test passed"
