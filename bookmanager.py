"""A small Flask + SQLAlchemy CRUD app for managing a list of book titles.

I built this to learn how Flask wires together with a database. It serves a
single page that lists the books I've stored and lets me add, rename, and
delete them, persisting everything to a local SQLite file.
"""

import os
from pathlib import Path

from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy

# Keep the SQLite file next to this module so the app behaves the same no
# matter which directory I launch it from. DATABASE_URL can override it (handy
# for tests), but it defaults to that local file.
PROJECT_DIR = Path(__file__).resolve().parent
DATABASE_URI = os.environ.get("DATABASE_URL", f"sqlite:///{PROJECT_DIR / 'bookdatabase.db'}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Book(db.Model):
    # A book is identified by its title, so I use the title itself as the
    # primary key and require it to be unique.
    title = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)

    def __repr__(self):
        return f"<Title: {self.title}>"


@app.route("/", methods=["GET", "POST"])
def home():
    # A POST means the add form was submitted; a GET just renders the list.
    if request.form:
        try:
            book = Book(title=request.form.get("title"))
            db.session.add(book)
            db.session.commit()
        except Exception as e:
            print("Failed to add book")
            print(e)
    books = Book.query.all()
    return render_template("home.html", books=books)


@app.route("/update", methods=["POST"])
def update():
    try:
        new_title = request.form.get("new_title")
        old_title = request.form.get("old_title")
        book = Book.query.filter_by(title=old_title).first()
        book.title = new_title
        db.session.commit()
    except Exception as e:
        print("Couldn't update book title")
        print(e)
    return redirect("/")


@app.route("/delete", methods=["POST"])
def delete():
    title = request.form.get("title")
    book = Book.query.filter_by(title=title).first()
    db.session.delete(book)
    db.session.commit()
    return redirect("/")


# Create the table on first import so the app is ready to use without a
# separate database-setup step.
with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
