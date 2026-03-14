# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **bug bounty workshop** built on a Django halftone image processor. The codebase contains **10 intentionally planted bugs** across different files for participants to find and fix. Bugs span signals, middleware, views, models, algorithms, and templates — some crash the app, some produce wrong output, some are silent, and two are visual. Each bug is in a different file; no file has more than 2 bugs.

## Common Commands

```bash
# Setup
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_workshop   # creates alice/bob/charlie with password: workshop2024

# Run
python manage.py runserver       # http://127.0.0.1:8000/

# Tests (test suite is private, pulled from Intuit-Toronto/django-box-tests during CI)
python manage.py test            # local tests are stubs
# CI runs: python run_single_bug.py <1-10> for each bug individually
```

## Architecture

**Django project** (`halftone_project/`) with two apps:

- **`accounts/`** — Registration, login/logout, user profile with halftone preferences (dot_spacing, style). `UserProfile` is created via a `post_save` signal on User. Profile preferences feed into halftone processing defaults.

- **`processor/`** — Core image processing app:
  - `halftone.py` — Standalone algorithm with 3 styles: classic (dots), diamond (color-aware), line. Grid-samples cells, computes brightness, draws proportional shapes.
  - `batch.py` — Synchronous batch processing of multiple images.
  - `utils.py` — Preset config validation (dot_spacing type, style enum).
  - `views.py` — Upload, result, gallery (with AJAX pagination), sharing (token-based public URLs), presets (create/import JSON), batch upload/status.
  - `models.py` — `ImageUpload` (with share tokens), `Preset` (JSON config), `BatchJob` (status tracking), `ActivityLog`.

**Middleware** (`halftone_project/middleware.py`):
- `ActivityLogMiddleware` — Logs authenticated requests to `ActivityLog` model.
- `RateLimitMiddleware` — Rate-limits POST to `/` based on `ActivityLog` counts. Middleware order is load-bearing (see settings.py comments).

**Key data flows:**
1. Upload: save original → apply_halftone() → save processed path → redirect to result
2. Batch: create BatchJob → save all images → process_batch() synchronously → update counts
3. Sharing: set `is_public=True` → auto-generate MD5 share token on save → public URL via token
4. Gallery: standard Paginator for HTML, cursor-based (`after` param) for AJAX

## Dependencies

Django 4.2–5.0, Pillow 10+. SQLite database. No async, no Celery, no Redis.

## CI

GitHub Actions (`.github/workflows/test.yml`) runs on PRs to main via `pull_request_target`. Tests are in a private repo and copied in at CI time. Each of the 10 bugs has a dedicated test step.
