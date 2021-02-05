import os

from flask import Blueprint
from flask import redirect, url_for, request, render_template, flash
from flask_login import current_user, login_required
from sonblog import db
from sonblog.posts.forms import PostForm
from sonblog.models import Posts

posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    postit = PostForm()
    if postit.validate_on_submit():
        dbpost = Posts(title=postit.title.data, content=postit.content.data, author=current_user)
        db.session.add(dbpost)
        db.session.commit()
        flash('Your post is sent to the Feed.', 'success')
        return redirect(url_for('main.home'))
    return render_template('createpost.html', title='New Post', form=postit)


@posts.route("/post/<int:post_id>")
def manage_post(post_id):
    mypost = Posts.query.get_or_404(post_id)
    return render_template('managepost.html', title=mypost.title, post=mypost)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Posts.query.get_or_404(post_id)
    if post.author != current_user:
        os.abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.manage_post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('createpost.html', title='Update Post', form=form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Posts.query.get_or_404(post_id)
    if post.author != current_user:
        os.abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))
