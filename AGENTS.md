# Agent Collaboration Guide

This repository contains multiple Mandarin tone trainer experiences. Keep changes scoped so parallel agents do not overwrite each other.

## Project Areas

- Adult cyberpunk trainer:
  - `public/tone_trainer-ponk.html`
  - Adult/cyberpunk-only assets should use `public/assets/ponk-*` names.

- Kids trainer:
  - `public/gulu-valley.html`
  - Kids-only assets should use `public/assets/gulu-*` names.

- Shared backend and data:
  - `server.py`
  - `data/trainer_data.private.json`
  - `data/access_codes.private.json`
  - `scripts/`

## Coordination Rules

1. Check `git status --short --branch` before editing.
2. Keep adult-trainer changes out of the kids page, and kids-trainer changes out of the adult page.
3. Do not edit shared backend or data files unless the change is intended to affect both versions.
4. Before changing shared files, review recent commits with `git log --oneline -5`.
5. Use clear commits that name the affected area, such as:
   - `Update cyberpunk trainer paywall copy`
   - `Add kids trainer lesson scene`
   - `Fix shared admin access logic`
6. If another agent has pushed changes, pull before continuing.
7. Do not remove or rename files owned by the other trainer without explicit user approval.

## Deployment Notes

Both trainers are served from the same Render app:

- Adult version: `/tone_trainer-ponk.html`
- Kids version: `/gulu-valley.html`
- Admin: `/admin`

Pushes to `main` may deploy both versions, so verify shared files carefully.
