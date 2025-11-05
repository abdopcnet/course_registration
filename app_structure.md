## Application structure — course_registration

Top-level layout (important files/directories)
- `manage.py` — Django CLI entry point.
- `course_registration/` — Django project package (settings, urls, views, wsgi/asgi).
  - `course_registration/settings.py` — central config (DB, templates, staticfiles, INSTALLED_APPS).
  - `course_registration/urls.py` — project URL routing; routes currently point to project-level views.
  - `course_registration/views.py` — simple page views that render templates (login, dashboard, materials, etc.).
- `courses/` — single installed app for domain logic. Current files:
  - `courses/models.py` — empty placeholder for DB models; add models here.
  - `courses/admin.py` — register models to expose in Django admin.
  - `courses/views.py` — app-specific view code (currently empty).
- `templates/` — top-level templates (not app-namespaced): `login.html`, `admin_dashbord.html`, `materials.html`, `students.html`, `sections.html`, `reports.html`.
- `static/` — static assets; referenced from `settings.py` via `STATICFILES_DIRS`.

Conventions and examples
- Page-first pattern: new pages are typically added by editing `course_registration/views.py`, creating a template in `templates/`, and mapping a URL in `course_registration/urls.py`.
  - Example: to add `/new-page/`:
    - Add `def new_page(request): return render(request, 'new_page.html')` to `course_registration/views.py`.
    - Create `templates/new_page.html`.
    - Add `path('new-page/', views.new_page, name='new_page')` to `course_registration/urls.py`.
- Domain data belongs in `courses/`. When adding a model:
  - Define model in `courses/models.py`.
  - Register in `courses/admin.py` with `admin.site.register(MyModel)`.
  - Run `python manage.py makemigrations` and `migrate`.

Notes about testing and CI
- No tests exist; add tests under `courses/tests.py` or a `tests/` folder. Use Django's test runner: `python manage.py test`.
- No CI config is present; if adding one, ensure DB setup for Postgres or use SQLite for test runs.
