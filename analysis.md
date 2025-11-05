## Codebase analysis — course_registration

Summary
- Small Django 4.2 project with the Django project at `course_registration/` and a single installed app `courses/`.
- Most current UI pages are implemented as simple project-level views in `course_registration/views.py` that render templates from the top-level `templates/` folder.

Key observations
- The `courses` app is scaffolded but contains no domain models yet (`courses/models.py` is empty). This indicates the project is in early development: UI scaffolding exists but business logic and persistence belong in `courses/`.
- Database configuration in `course_registration/settings.py` uses PostgreSQL with credentials stored in the settings file. These are sensitive and should be moved to environment variables for production or PR hygiene.
- Templates are not namespaced by app and live under a single `templates/` directory. This simplifies rendering but requires unique filenames to avoid collisions.

Where to make changes
- Add pages: `course_registration/views.py` + `templates/` + `course_registration/urls.py`.
- Add domain logic/models: `courses/models.py` + admin registration in `courses/admin.py` + migrations.

Quick risks & recommendations
- Secrets in `settings.py`: extract `SECRET_KEY` and DB credentials to env vars and add `.env.example` to repo (do not commit live secrets).
- Tests: no tests present. Add at least one smoke test that imports `course_registration` and checks a route or renders a template.
- Local dev: settings expect Postgres. For quick iteration consider adding a fallback SQLite config when an env var is set.

Immediate next tasks (low risk)
- Replace DB credentials with environment variables and add `requirements.txt`.
- Add a minimal model in `courses/models.py` (e.g., Course) and a corresponding admin registration to verify migrations.
- Add `python manage.py test` target with one simple view test.
