import copy
from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app
from flask_login import login_required, current_user
from sqlalchemy import desc
from app import db
from comments.forms import CommentForm
from forum.forms import ForumForm
from models import Forum, Comments

forum_blueprint = Blueprint('forum', __name__, template_folder='templates')


@forum_blueprint.route('/forum')
@login_required
def forum():
    posts = Forum.query.order_by(desc('post_id')).all()
    return render_template('forum.html', forum=posts, user=current_user)


@forum_blueprint.route('/create', methods=('GET', 'POST'))
def create():
    form = ForumForm()

    if form.validate_on_submit():
        new_post = Forum(user_id=current_user.id, title=form.title.data, body=form.body.data)

        db.session.add(new_post)
        db.session.commit()

        return forum()
    return render_template('create_forum.html', form=form)


@forum_blueprint.route('/<int:post_id>/update', methods=('GET', 'POST'))
def update(post_id):
    post = Forum.query.filter_by(post_id=post_id).first()
    if not post:
        return render_template('500.html')

    form = ForumForm()

    if form.validate_on_submit():
        Forum.query.filter_by(post_id=post_id).update({"title": form.title.data})
        Forum.query.filter_by(post_id=post_id).update({"body": form.body.data})

        db.session.commit()

        return forum()

    # creates a copy of post object which is independent of database.
    post_copy = copy.deepcopy(post)

    # set update form with title and body of copied post object
    form.title.data = post_copy.title
    form.body.data = post_copy.body

    return render_template('update_forum.html', form=form)


@forum_blueprint.route('/<int:post_id>/delete')
def delete(post_id):
    Forum.query.filter_by(post_id=post_id).delete()
    Comments.query.filter_by(post_id=post_id).delete()
    db.session.commit()

    return forum()


@forum_blueprint.route('/<int:post_id>/comment', methods=('GET', 'POST'))
def comment(post_id):
    post = Forum.query.filter_by(post_id=post_id).first()
    form = CommentForm()
    if form.validate_on_submit():

        new_comment = Comments(body=form.body.data, user_id=current_user.id, post_id=post_id)

        db.session.add(new_comment)
        db.session.commit()

        return forum()
    return render_template('create_comment.html', form=form)


@forum_blueprint.route('/<int:post_id>/view_comments')
def view_comments(post_id):
    comments = Comments.query.filter_by(post_id=post_id).order_by(desc('post_id')).all()
    return render_template('view_comments.html', comment=comments, post_id=post_id)


@forum_blueprint.route('/<int:comment_id><int:post_id>/delete_comment')
def delete_comment(comment_id, post_id):
    Comments.query.filter_by(comment_id=comment_id).delete()
    db.session.commit()

    return view_comments(post_id)



