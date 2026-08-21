# Architecture et protocole

[🇫🇷 Français](workflow.md) · [🇬🇧 English](../../workflow.md)

## 1. Challenge avant action

Toute demande non triviale est classée avant le travail :

- `SKIP` pour une modification courte, réversible et clairement vérifiable ;
- `EXPLORE` lorsque la lecture du dépôt peut lever l'incertitude ;
- `DECIDE` lorsqu'un choix de produit, de sécurité, de coût ou d'autorité est nécessaire.

Le challenge formule le résultat attendu, les hypothèses et la validation. Il ne remplace ni l'analyse de code ni les tests.

## 2. Routage des agents et de l'inférence

Les skills versionnées sont dans `.codex/skills/` : `$intent-challenger`, `$adaptive-model-router` et `$claude-review-gate`. Elles constituent l'orchestrateur du workflow ; aucun script ne remplace ou ne télécharge un modèle.

Le routeur conserve Terra/Medium comme écrivain principal. Il réserve Luna/Low aux recherches ciblées ou opérations mécaniques, Terra/High aux diagnostics et revues difficiles, et Sol/High aux problèmes critiques (sécurité, intégrité, concurrence, migration ou ambiguïté d'architecture). Il reste mono-agent lorsque le parallélisme n'apporte aucun gain réel, limite la délégation à quatre agents, et interdit deux écrivains sur les mêmes fichiers.

## 3. Un seul écrivain

Codex est l'unique processus autorisé à modifier le worktree. Claude ne reçoit jamais l'autorisation d'éditer, d'écrire, de naviguer sur le Web ou d'appeler des MCP. Cette séparation évite les écritures concurrentes et rend l'auteur de chaque correction explicite.

## 4. Paquet de revue borné

`build-review-packet.py` collecte les fichiers modifiés et non suivis, exclut les répertoires lourds et les fichiers `.env`, puis génère :

- `review-packet.md`, la portée et les règles ;
- `review-diff.patch`, un diff limité à 24 k caractères en rapide, 180 k en profond ;
- `scope.json`, le mode, les fichiers, l'heuristique de risque et une empreinte SHA-256 de chaque fichier.

Le mode profond est choisi automatiquement lorsqu'un nom de fichier indique une frontière sensible, que plus de 12 fichiers source sont modifiés ou que le diff dépasse 1 200 lignes. Ces heuristiques sont des garde-fous, pas une classification de sécurité exhaustive.

## 5. Verdict indépendant

Claude doit retourner uniquement le JSON défini dans `schemas/findings.schema.json`. Le lanceur rejette les formats incomplets, les champs supplémentaires et les verdicts contradictoires. Il vérifie également que l'état Git n'a pas changé pendant la revue.

## 6. Boucle de correction

Un `FAIL` arrête le gate avec le code 3. L'agent ou la personne qui implémente :

1. vérifie les preuves ;
2. écarte les faux positifs ;
3. corrige la cause racine des constats valides ;
4. lance les tests adaptés ;
5. relance une revue.

Le lanceur ne corrige pas automatiquement un `FAIL`. C'est un choix délibéré : une conclusion de revue n'est pas une instruction exécutable.
