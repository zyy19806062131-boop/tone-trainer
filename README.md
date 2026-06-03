# Mandarin Tone Trainer

Cyberpunk Mandarin tone trainer with backend code-based access.

## Run Locally

```bash
python3 server.py
```

Then open:

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

For deployment, set the `ADMIN_CODE` environment variable in your host dashboard.

## Edit Access Codes

Edit:

```text
data/access_codes.private.json
```

Example:

```json
{
  "studentA2026": {
    "label": "STUDENT A",
    "decks": ["cafe", "e1"]
  }
}
```

Use `"decks": "all"` to allow every project.

## Edit Training Projects

Edit:

```text
data/trainer_data.private.json
```

Each project is a deck:

```json
{
  "id": "cafe",
  "name": "咖啡生存口语",
  "full": true,
  "sents": []
}
```

The `id` is what access codes reference.

## Important

Use a private GitHub repository if you want to keep access codes, training content, or embedded voice audio hidden from the public.

GitHub Pages alone is not enough for protected login because it only serves static files. This project needs the Python backend in `server.py`, so deploy it to a backend host such as Render, Railway, Fly.io, or a VPS.
