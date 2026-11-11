# EGS skills repository

This repository holds EGS's Claude skills as plugins: `plugins/egs-core` for everyone, and one plugin
per role. The marketplace file is `.claude-plugin/marketplace.json`.

If you are helping someone use the skills, load the egs skill (in egs-core) and, for setup, the
egs-connect skill.

## If you are changing a skill

- Write everything as EGS's own way of working, for EGS's team.
- Read-only stays the rule: the readers in `plugins/egs-core/scripts/` never write to any system,
  the guard keeps blocking write tools, and no instruction may tell a Claude to send, post or change
  anything.
- Keep each `SKILL.md` short; detail goes in that skill's `references/`.
- Bump the plugin's `version` when you change it, or installed copies will not update.
- Validate before sharing: `claude plugin validate .` and `claude plugin validate plugins/<name>`.
  Run a case from `evals/` after any change to the sweep.
- Changes reach the team through a pull request reviewed by the project manager.
