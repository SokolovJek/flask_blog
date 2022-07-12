from flask import (request, render_template, url_for, flash, redirect, abort, Blueprint)
from flask_login import current_user, login_required
from flask_blog import db
from flask_blog.posts.forms import PostForm
from flask_blog.models import Post

posts = Blueprint('posts', __name__)


@login_required
@posts.route('/all_posts')
def all_posts():
    """
    Контролер для отображения всех постов
    """
    # палучение параметров, если нет то ставим подефолту 1
    page = request.args.get('page', 1, type=int)
    # настройка пагинации - вывод на странице по пять постов
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('all_posts.html', posts=posts)


@login_required
@posts.route('/post/new', methods=['GET', 'POST'])
def new_post():
    """
    Контролер для создания нового поста
    """
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    content=form.content.data,
                    author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Ваш пост создан!', 'success')
        return redirect(url_for('posts.all_posts'))
    return render_template('create_post.html', form=form, legend='Новый пост')


@login_required
@posts.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    """
    Контролер для просмотра конкретного поста
    """
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@login_required
@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
def update_post(post_id):
    """
    Контролер для обновления поста
    """
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Ваш пост обнавлен!', 'success')
        return redirect(url_for('posts.post', post_id=post_id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        flash('Ваш пост создан!', 'success')
        return render_template('create_post.html', form=form, legend='Обновление поста', title='Обновление поста')


@login_required
@posts.route('/post/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """
    Контролер для удаления поста
    """
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Ваш пост удален!', 'success')
    return redirect(url_for('posts.all_posts'))
