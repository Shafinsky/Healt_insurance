# Health Insurance

A web application for managing health insurance records: clients, insurance policies and insurance claims.

## Features

- User registration and login (email + password, hashed with Werkzeug)
- Role-based access: regular **user** and **admin**
- Manage **clients** (create / edit / delete, admin-only)
- Manage **insurance policies** (create / edit / delete)
- Submit and manage **insurance claims**
- Admin panel: view users, promote users to admin, delete users
- Claim approval / rejection workflow with **email notifications** (Flask-Mail)
- Server-side rendered HTML templates with WTForms validation

## Tech stack

- **Flask** — web framework
- **Flask-SQLAlchemy** — ORM and database access
- **Flask-Login** — user sessions and authentication
- **Flask-Migrate** (Alembic) — database migrations
- **Flask-Mail** — email notifications
- **Flask-WTF / WTForms** — form rendering and validation
- **Werkzeug** — password hashing

## Domain model

- **User** — account with a role (`user` / `admin`)
- **Client** — insured person
- **Policy** — insurance policy, linked to clients (many-to-many)
- **Claim** — insurance claim with a status (`Pending` / `Approved` / `Rejected`)

## Project structure

app.py 
### Flask app factory (create_app) 
extensions.py 
### db, login_manager, migrate, mail instances 
models.py 
### SQLAlchemy models (User, Client, Policy, Claim) 
routes.py 
### main blueprint (clients, policies, claims, admin) 
auth.py 
### auth blueprint (register, login, logout) 
forms.py 
### WTForms forms 
utils.py 
### role helpers (is_admin) 
wsgi.py 
### WSGI entry point 
config.py 
### app configuration (local, not committed) 
templates/ 
### Jinja2 HTML templates 
migrations/ 
### Alembic migration scripts

> **Note:** `config.py` is git-ignored (listed as `.config.py` in `.gitignore`). Create it locally with your database URI, secret key and mail settings before running.

## Getting started

1. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   pip install flask flask-sqlalchemy flask-login flask-migrate flask-mail flask-wtf

2. Create config.py with your database URI, SECRET_KEY and mail settings.
3. Apply migrations:
   ```bash
   flask db upgrade
5. Run the app:
   ```bash
   python wsgi.py
7. Open http://localhost:5000
