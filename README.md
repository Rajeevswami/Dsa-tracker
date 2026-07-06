# DSA Tracker — LeetCode Progress Tracker

A Django app to track your 8-week DSA interview prep roadmap. Tracks per-problem
status, difficulty, and schedules **spaced-repetition revision dates** automatically
when you mark a problem solved.

## Features
- 8-week roadmap pre-seeded (70 curated problems across Arrays, LinkedList, Trees,
  Graphs, DP, Backtracking, Heaps/Tries)
- Mark problems: Attempted / Solved / Needs Revision
- Auto revision scheduling: 1st solve → revise in 3 days, 2nd → 7 days, 3rd+ → 14 days
- Dashboard with overall % progress, filter by status/difficulty
- "Due for revision today" banner
- Django admin to add/edit your own problems and topics

## Tech Stack
Django 6, SQLite (dev) / PostgreSQL (prod via `dj-database-url`), Bootstrap 5,
Gunicorn + WhiteNoise for deployment — same stack pattern as your HMS project.

## Local Setup

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run migrations
python manage.py migrate

# 4. Seed the 8-week roadmap (adds 8 topics + 70 problems)
python manage.py seed_roadmap

# 5. Create your login
python manage.py createsuperuser

# 6. Run the server
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` and log in with the superuser you created.

## Adding Your Own Problems
Go to `http://127.0.0.1:8000/admin/` → log in → add problems under any Topic,
or add new Topics for extra weeks (e.g. revision weeks, company-specific sheets).

## Project Structure
```
leetcode_tracker/
├── config/              # Django project settings, root urls
├── progress/            # Main app
│   ├── models.py        # Topic, Problem, ProgressEntry
│   ├── views.py         # dashboard, mark_status, update_notes
│   ├── urls.py
│   ├── admin.py
│   ├── management/commands/seed_roadmap.py   # seeds 8-week plan
│   └── templates/progress/
├── requirements.txt
├── Procfile             # for Render
└── manage.py
```

## Deploying to Render (same flow as your HMS project)

1. Push this project to a GitHub repo.
2. On Render: **New → Web Service** → connect the repo.
3. Build command:
   ```
   pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
   ```
4. Start command:
   ```
   gunicorn config.wsgi:application
   ```
5. Add environment variables on Render:
   - `SECRET_KEY` — generate a new one (don't reuse the dev one)
   - `DEBUG` = `False`
   - `ALLOWED_HOSTS` = `your-app.onrender.com`
   - `DATABASE_URL` — Render auto-fills this if you attach a Render PostgreSQL instance
6. After first deploy, run `seed_roadmap` once via Render's shell tab:
   ```
   python manage.py seed_roadmap
   python manage.py createsuperuser
   ```

## Extending Ideas (good portfolio talking points)
- Add a `notes` field UI (model already supports it) for storing your approach/mistakes per problem
- Add a streak counter (consecutive days with at least 1 solve)
- Add a company-tag field on `Problem` (e.g. "Google", "Amazon") for company-wise filtering
- Add REST API endpoints with DRF so you could build a mobile companion later
