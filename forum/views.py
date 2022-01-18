import copy
from flask import Blueprint, render_template, flash, redirect, url_for, request, current_app
from flask_login import login_required, current_user
from sqlalchemy import desc
from comments.forms import CommentForm
from forum.forms import ForumForm
from models import Forum, Comments, db

forum_blueprint = Blueprint('forum', __name__, template_folder='templates')


# function to display the main forum page
@forum_blueprint.route('/forum')
@login_required
def forum():
    posts = Forum.query.order_by(desc('post_id')).all()
    return render_template('forum.html', forum=posts, user=current_user)


# function to create a new forum
@forum_blueprint.route('/create', methods=('GET', 'POST'))
def create():
    # run the form to obtain user input
    form = ForumForm()

    if form.validate_on_submit():
        new_post = Forum(user_id=current_user.id, title=form.title.data, body=form.body.data)

        # commit changes to database
        db.session.add(new_post)
        db.session.commit()

        # display forum home page
        return forum()
    # if the form is not validated then render the create_forum template again
    return render_template('create_forum.html', form=form)


# function to update already created forums
@forum_blueprint.route('/<int:post_id>/update', methods=('GET', 'POST'))
def update(post_id):
    post = Forum.query.filter_by(post_id=post_id).first()
    if not post:
        return render_template('error_codes/500.html')

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


# function to delete forum posts
@forum_blueprint.route('/<int:post_id>/delete')
def delete(post_id):
    Forum.query.filter_by(post_id=post_id).delete()
    Comments.query.filter_by(post_id=post_id).delete()
    db.session.commit()

    return forum()


# function to add a comment to a forum post
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


# function to display all comments on a given forum post
@forum_blueprint.route('/<int:post_id>/view_comments')
def view_comments(post_id):
    comments = Comments.query.filter_by(post_id=post_id).order_by(desc('post_id')).all()
    return render_template('view_comments.html', comment=comments, post_id=post_id)


# function to delete any comments on a post
@forum_blueprint.route('/<int:comment_id><int:post_id>/delete_comment')
def delete_comment(comment_id, post_id):
    Comments.query.filter_by(comment_id=comment_id).delete()
    db.session.commit()

    return view_comments(post_id)
