# Agent Collaboration Guide

This repository contains the Mandarin tone trainer app. Keep changes scoped so parallel agents do not overwrite each other.

## Project Areas

- Cyberpunk trainer:
  - `public/tone_trainer-ponk.html`
  - Trainer-specific assets should use `public/assets/ponk-*` names.

- Shared backend and data:
  - `server.py`
  - `data/trainer_data.private.json`
  - `data/access_codes.private.json`
  - `scripts/`

## Coordination Rules

1. Check `git status --short --branch` before editing.
2. Keep trainer UI changes scoped to `public/tone_trainer-ponk.html` unless shared behavior is required.
3. Do not edit shared backend or data files unless the change is intended to affect both versions.
4. Before changing shared files, review recent commits with `git log --oneline -5`.
5. Use clear commits that name the affected area, such as:
   - `Update cyberpunk trainer paywall copy`
   - `Add kids trainer lesson scene`
   - `Fix shared admin access logic`
6. If another agent has pushed changes, pull before continuing.
7. Do not reintroduce removed experimental pages without explicit user approval.

## Deployment Notes

The trainer is served from the Render app:

- Main version: `/tone_trainer-ponk.html`
- Admin: `/admin`

Pushes to `main` deploy the app, so verify shared files carefully.
