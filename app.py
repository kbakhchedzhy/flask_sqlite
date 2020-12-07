from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

"""
database:
CREATE TABLE posts (Id int PRIMARY KEY AUTOINCREMENT, title varchar(150), description text, date date);
"""


@app.route('/')
def output_list():
    """
    Main page, which output all posts from database.
    :return: posts
    """
    connection = sqlite3.connect('blog.sqlite')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM posts;")
    posts = cursor.fetchall()
    connection.close()
    return render_template('index.html', posts=posts)


@app.route('/add')
def insert_in_list():
    """
    This page will add new post. Require title and description. Date will be today.
    :return: redirect on main page
    """
    title = request.args.get('title')
    description = request.args.get('text')
    connection = sqlite3.connect('blog.sqlite')
    cursor = connection.cursor()
    values = (title, description)
    cursor.execute("INSERT INTO posts (title, description, date) VALUES (?, ?, current_date );", values)
    connection.commit()
    connection.close()
    return redirect('/')


@app.route('/update')
def update_list():
    """
    Update posts. Require id, text, describe. Can't update without id. Date doesn't update.
    :return: redirect on main page
    """
    try:
        id_of_post = request.args['id']
        title = request.args.get('title')
        description = request.args.get('text')
        connection = sqlite3.connect('blog.sqlite')
        cursor = connection.cursor()
        if not title:
            values = (description, id_of_post)
            cursor.execute("UPDATE posts SET description = ? WHERE id = ?;", values)
        elif not description:
            values = (title, id_of_post)
            cursor.execute("UPDATE posts SET title = ? WHERE id = ?;", values)
        else:
            values = (title, description, id_of_post)
            cursor.execute("UPDATE posts SET title = ?, description = ? WHERE id = ?;", values)
        connection.commit()
        connection.close()
        return redirect('/')
    except KeyError:
        return '<h3>Ошибка. Введите id.</h3>'


@app.route('/delete')
def delete_post():
    """
    Update posts. Require only id.
    :return: redirect on main page
    """
    try:
        id_of_post = request.args['id']
        connection = sqlite3.connect('blog.sqlite')
        cursor = connection.cursor()
        cursor.execute("DELETE FROM posts WHERE id = ?;", id_of_post)
        connection.commit()
        connection.close()
        return redirect('/')
    except KeyError:
        return '<h3>Ошибка. Введите id.</h3>'


if __name__ == '__main__':
    app.run(debug=True)
