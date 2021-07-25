from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from mooder.auth import login_required
from mooder.db import get_db

bp = Blueprint('mood', __name__)

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, mood,title, body, created, author_id, username'
        ' FROM moods p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('moods/index.html', posts=posts,mooddir={1:'\U0001F603',
                                                                    2:'\U0001F606',
                                                                    3:'\U0001F610',
                                                                    4:'\U0001F614',
                                                                    5:'\U0001F616'})


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        mood =request.form['mood']
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'
        
        if not mood:
            error = 'Mood is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO moods (mood,title, body, author_id)'
                ' VALUES (?, ?, ?, ?)',
                (mood,title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('mood.index'))

    return render_template('moods/create.html')

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, mood, title, body, created, author_id, username'
        ' FROM moods p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        mood = request.form['mood']
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if not mood:
            error = 'Mood is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE moods SET mood=?,title = ?, body = ?'
                ' WHERE id = ?',
                (mood,title, body, id)
            )
            db.commit()
            return redirect(url_for('mood.index'))

    return render_template('moods/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM moods WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('mood.index'))