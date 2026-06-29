# Mandarin Tone Trainer

Mandarin tone training app with a Python backend, code-based access control, optional PostgreSQL storage, and built-in support for browser fallback speech.

## Features

- Tone-by-tone sentence playback with embedded audio or browser TTS fallback
- Admin UI for access codes, projects, units, and sentence content
- Local JSON storage by default, with PostgreSQL support when `DATABASE_URL` is set
- Audio generation helper for HSK and YCT decks

## Run Locally

```bash
python3 server.py
```

Open:

```text
http://127.0.0.1:8765/tone_trainer-ponk.html
```

Admin page:

```text
http://127.0.0.1:8765/admin
```

Default local admin code:

```text
admin2026
```

Set `ADMIN_CODE` in your environment to change it in deployment.

## Sample Access

The repository includes a small sample project and a sample access code so the app runs out of the box after cloning.

Sample code:

```text
sample2026
```

## Build Voice Audio

HSK decks use female and male voices. YCT decks use the child voice.

```bash
python3 scripts/build_project_audio.py --deck hsk1
python3 scripts/build_project_audio.py --deck yct1
```

Use `--force` to regenerate existing audio.

## Data Files

- `data/access_codes.private.json`: access code to project mapping
- `data/trainer_data.private.json`: projects, units, sentences, and optional embedded audio

## Deployment

GitHub Pages is not enough for protected login because it only serves static files. Deploy `server.py` to a backend host such as Render, Railway, Fly.io, or a VPS.

## License

MIT. See [`LICENSE`](LICENSE).
