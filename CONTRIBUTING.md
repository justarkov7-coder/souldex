# Contribuer

[🇫🇷 Français](CONTRIBUTING.md) · [🇬🇧 English](CONTRIBUTING.en.md)

1. Ne commite aucune donnée personnelle, secret, journal de revue ou chemin de machine.
2. Maintiens la séparation des rôles : le script ne doit jamais donner une capacité d'écriture à Claude.
3. Exécute les contrôles ci-dessous avant une pull request.

```bash
bash -n bin/ai-review-loop bin/ai-review-await install.sh
python3 -c "compile(open('bin/build-review-packet.py', encoding='utf-8').read(), 'bin/build-review-packet.py', 'exec')"
bash tests/smoke.sh
```

Les changements du protocole ou des permissions nécessitent une revue humaine explicite, car ils modifient la frontière de sécurité.
