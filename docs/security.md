# Modèle de sécurité

[🇫🇷 Français](security.md) · [🇬🇧 English](security.en.md)

## Données et publication

Ce dépôt ne doit contenir ni journaux de revue, ni `.env`, ni jeton, ni réglage Claude/Codex personnel. Les chemins utilisateur sont résolus à l'exécution via `$HOME` et les ressources du package sont résolues relativement au script.

Avant un fork ou une contribution, lance :

```bash
git grep -nE '(/Users/|/home/|API[_-]?KEY|AUTH[_-]?TOKEN|GITHUB_TOKEN|BEGIN (RSA|OPENSSH))' || true
```

Tout résultat doit être soit supprimé, soit un nom de variable documenté sans valeur. N'ajoute jamais les artefacts sous `~/.local/state/codex-claude-review`.

## Configuration Claude requise

Copie les principes de `config/claude-settings.example.json` dans la configuration Claude de ton choix : sandbox activée, échec si elle est indisponible, écriture refusée et identifiants cloud/registre refusés. Ajuste les chemins temporaires pour ton système. Ne copie pas un fichier de réglages personnel dans ce dépôt.

Le lanceur passe aussi `--disallowedTools` pour bloquer les outils d'écriture, le Web, les questions interactives et les MCP. Cette défense en profondeur ne remplace pas la configuration de sandbox : le `--dry-run` vérifie seulement les CLI et ressources locales ; confirme aussi visuellement que ta configuration Claude applique la sandbox.

## Frontières assumées

- Claude reçoit le prompt, le paquet et le diff de revue : ne l'utilise pas sur du code ou des données que ta politique interdit d'envoyer au fournisseur.
- Le mode profond peut lire les fichiers nécessaires à l'analyse dans la sandbox Claude. Le mode rapide n'utilise aucun outil.
- Les vérifications CI et une revue humaine restent nécessaires pour les changements critiques.
