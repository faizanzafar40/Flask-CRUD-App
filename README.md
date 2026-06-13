# CRUD Web App

A small Flask web app for managing a list of book titles — create, read, update, and delete.

I built this to learn how Flask wires together with a database. It serves a single page that lists
the books I've stored and lets me add, rename, and delete them, persisting everything to a local
SQLite file through Flask-SQLAlchemy.

## Tech stack

- **Python 3**
- **Flask** — web framework and routing
- **Flask-SQLAlchemy / SQLAlchemy** — ORM and database access
- **SQLite** — file-based storage, created automatically on first run
- **pytest** — smoke tests
- **Ruff** — linting and formatting

## Features

- List every book on the home page
- Add a book with the title form
- Rename a book inline
- Delete a book inline

Each title is unique and acts as the record's primary key.

## Sample output

The home page shows the add form above a table of books, each row with its own Update and Delete
controls. To include a screenshot, drop an image at `docs/screenshot.png` and reference it here:

<!-- ![Home page](docs/screenshot.png) -->

## Prerequisites

- Python 3.9 or newer

## Installation

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

## Running the app

```bash
python bookmanager.py
```

Then open http://127.0.0.1:5000 in a browser. The SQLite database (`bookdatabase.db`) is created
automatically next to `bookmanager.py` on first run. Set the `DATABASE_URL` environment variable to
point at a different SQLite location if you'd like.

## Running the tests

```bash
pip install -r requirements-dev.txt
pytest
```

## Project structure

```
CRUD-Web-App/
├── bookmanager.py            # Flask app: routes, model, and configuration
├── templates/
│   └── home.html             # Single page: add form + book table
├── tests/
│   └── test_bookmanager.py   # CRUD smoke tests
├── requirements.txt          # Runtime dependencies
├── requirements-dev.txt      # Test/dev dependencies
└── pyproject.toml            # Ruff configuration
```

## What I learned

This was my first hands-on look at building a web app end to end: defining routes, rendering a
Jinja template, and backing it all with a database through an ORM. It gave me a feel for the request
cycle and for how SQLAlchemy models map to tables — a foundation I can reuse for larger Flask
projects.
