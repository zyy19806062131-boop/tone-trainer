# Agent Collaboration Guide

This repository contains the Mandarin tone trainer app. Keep changes scoped so parallel agents do not overwrite each other.

## Content Handoffs (read before touching lesson data)

Lesson content lives in `data-source/*_kewen_source.py` (transcribed from textbooks) and is
compiled into `data/trainer_data.private.json`. Before editing or extending any deck, read:

- [`HANDOFF_HSK1.md`](HANDOFF_HSK1.md) — decks `hsk1` (旧版标准教程) and `nhsk1` (新版 HSK3.0), 353 sentences.
- [`HANDOFF_HSK2.md`](HANDOFF_HSK2.md) — deck `nhsk2` (新版 HSK2), 348 sentences, 2026-08-05.
  **Its section 5 is required reading before adding HSK3/4**: naive silence-segment counting
  misaligns audio *silently*; only the ASR-verified aligner is trustworthy. It also documents
  why a new deck must NOT be named `hsk3` (`apply_data_migrations()` would overwrite it).

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
