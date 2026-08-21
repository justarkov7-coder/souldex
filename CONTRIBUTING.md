# Contributing

[🇫🇷 Français](docs/i18n/fr/CONTRIBUTING.md) · [🇬🇧 English](CONTRIBUTING.md)

1. Never commit personal data, a secret, a review log, or a machine-specific path.
2. Preserve role separation: the scripts must never give Claude write capability.
3. Run these checks before opening a pull request.

```bash
bash -n bin/ai-review-loop bin/ai-review-await install.sh
python3 -c "compile(open('bin/build-review-packet.py', encoding='utf-8').read(), 'bin/build-review-packet.py', 'exec')"
bash tests/smoke.sh
```

Changes to the protocol or permissions need explicit human review because they change the security boundary.
