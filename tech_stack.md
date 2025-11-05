## Tech stack — course_registration

Overview
- Core framework: Django (4.2.x). The project header shows Django 4.2.25 was used to generate settings.
- Language: Python (workspace `.venv` shows Python 3.9 site-packages). Aim for Python 3.9+.
- Database: PostgreSQL (configured in `course_registration/settings.py`).

Key components and packages to install
- Django — the web framework (4.2.x).
- psycopg2-binary — Postgres DB driver for local development.
- python-dotenv (optional) — load environment variables from a `.env` file in development.
- gunicorn (production) — WSGI HTTP server for deployment.
- whitenoise (optional) — serve static files in production if not using a CDN.

Recommended minimal `requirements.txt` (create at repo root)

```
Django>=4.2,<4.3
psycopg2-binary>=2.9
python-dotenv>=0.21
gunicorn>=20.1
whitenoise>=6.5
```

Local dev setup (quick)

1. Create and activate a venv (zsh):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Database: project uses PostgreSQL by default. Either:
- Ensure Postgres is running and create a DB named `course_registration` matching `settings.py`, or
- Temporarily switch to SQLite for quick local runs by editing `course_registration/settings.py` (development-only change).

3. Run migrations and start dev server:

```bash
python manage.py migrate
python manage.py runserver
```

Testing
- Use Django test runner: `python manage.py test`.

Production notes
- Do NOT commit `SECRET_KEY` or DB credentials. Move them to environment variables and use `python-dotenv` or container/host envs.
- Use `gunicorn` with an appropriate process manager (systemd, supervisor, or container) behind a reverse proxy (nginx).
- Serve static files via CDN or `whitenoise` + compressed assets; collect static with `python manage.py collectstatic`.

Where these items appear in the repo
- `course_registration/settings.py` — DB, templates, staticfiles settings; replace hard-coded secrets with env vars.
- `manage.py` — CLI entry used to run migrations, tests, and devserver.

If you want, I can:
- Add a `requirements.txt` with pinned versions.
- Add an `.env.example` and a small `settings_local.py` pattern that reads env vars.
- Add a Dockerfile and docker-compose for local Postgres + app (if you prefer containerized dev).
