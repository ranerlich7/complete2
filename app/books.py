import os
import sqlite3
from flask import Blueprint, Flask, render_template, request, redirect

con = sqlite3.connect("books.db", check_same_thread=False)
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS books (title, author, genre, year)")
con.commit()

books_bp = Blueprint('books', __name__, url_prefix='/books')

@books_bp.route("/")
def books():
    result = cur.execute("SELECT *,rowid from books").fetchall()
    return render_template("books.html", books=result)


@books_bp.route("/deletebook")
def deletebook():
    id = request.args.get('id')
    cur.execute(f"DELETE FROM books WHERE rowid={id};")
    con.commit()
    return redirect("/?message=Book Deleted")

@books_bp.route("/addbookindb", methods=['POST'])
def addbook_indb():
    from app.main import app

    title = request.form.get('title')
    author = request.form.get('author')
    genre = request.form.get('genre')
    year = request.form.get('year')
    file = request.files['file']
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

    print(f"INSERT INTO books VALUES ('{title}', '{author}', '{genre}', '{year}')")
    cur.execute(f"INSERT INTO books VALUES ('{title}', '{author}', '{genre}', '{year}')")
    con.commit()
    return redirect("/?message=Book Added")

@books_bp.route("/addbook")
def addbook():
    return render_template("addbook.html")

