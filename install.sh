#!/usr/bin/env bash
set -euo pipefail

source_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
prefix="${AI_REVIEW_INSTALL_PREFIX:-$HOME/.local}"
bin_dir="$prefix/bin"
share_dir="$prefix/share/codex-claude-review-gate"

mkdir -p "$bin_dir" "$share_dir"
for directory in bin prompts schemas config; do
  rm -rf "$share_dir/$directory"
  cp -R "$source_dir/$directory" "$share_dir/$directory"
done
chmod +x "$share_dir/bin/ai-review-loop" "$share_dir/bin/ai-review-await" "$share_dir/bin/build-review-packet.py"
ln -sfn "$share_dir/bin/ai-review-loop" "$bin_dir/ai-review-loop"
ln -sfn "$share_dir/bin/ai-review-await" "$bin_dir/ai-review-await"
printf 'Installed in %s\nAdd %s to PATH if needed.\nRead README.md before enabling Claude review permissions.\n' "$share_dir" "$bin_dir"
