import os
import sqlite3
from flask import Blueprint, Flask, render_template, request, redirect, url_for
from app.upload import upload_file

con = sqlite3.connect("books.db", check_same_thread=False)
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS books (title, author, genre, year)")
con.commit()

# def change_table():
#     cur.execute("ALTER TABLE books ADD filename ")
#     con.commit()
# change_table()

books_bp = Blueprint('books', __name__, url_prefix='/books')

@books_bp.route("/")
def books():
    result = cur.execute("SELECT *,rowid from books")
    new_result = []
    for book in result:
        new_result.append({
            'title' : book[0],
            'author': book[1],
            'genre': book[2],
            'year': book[3],
            'filename': f'uploads/{book[4]}',
            'id': book[5]
        })
    return render_template("books.html", books=new_result)


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
    filename=upload_file(request)
    print(f"filename is:{filename}")
    print(f"INSERT INTO books VALUES ('{title}', '{author}', '{genre}', '{year}', '{filename}')")
    cur.execute(f"INSERT INTO books VALUES ('{title}', '{author}', '{genre}', '{year}', '{filename}')")
    con.commit()
    return redirect("/?message=Book Added")

@books_bp.route("/addbook")
def addbook():
    return render_template("addbook.html")

