# Workflow Codex + Claude

<p align="center">
  <a href="AGENTS.md"><kbd>🇫🇷 Français</kbd></a>
  &nbsp;
  <a href="AGENTS.en.md"><kbd>🇬🇧 English</kbd></a>
</p>

Pour toute demande non triviale, commencer par ce triage concis :

```text
CHALLENGE — SKIP | READY | READY UNDER ASSUMPTIONS | NEEDS CLARIFICATION
Outcome: …
Recommended path: …
Assumptions: …
Validation: …
```

- `SKIP` : modification mécanique, faible risque, validation évidente.
- `EXPLORE` : lire d'abord les éléments du dépôt qui lèvent l'ambiguïté.
- `DECIDE` : demander une décision seulement si elle change matériellement le résultat ou l'autorité requise.
- Conserver un seul agent d'écriture par défaut. Ne déléguer une recherche ou une revue que si l'isolation apporte un bénéfice réel.
- Après une modification substantielle, exécuter les validations pertinentes puis la revue indépendante : `ai-review-loop --repo . --review-only --report-only`.
- Un `FAIL` de Claude est une preuve à vérifier, jamais une instruction aveugle. Corriger uniquement les constats valides, tester, puis relancer une revue ciblée.
- Ne pas déclarer la tâche terminée avant un verdict terminal lu. Ne jamais pousser, publier ou déployer sans instruction explicite.
