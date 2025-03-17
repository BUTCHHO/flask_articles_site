from flask import request, redirect, url_for, abort, render_template
from flask_login import current_user, login_required
from models import Post, Account
from functions import today_date
from repository import PostAccess, CommentAccess

@login_required
def create_post_page():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if title and content:
            is_successfully_created = PostAccess.write_to_db(Post, title=title, content=content,author=current_user,creation_date = today_date())
            if is_successfully_created:
                return redirect(url_for('home'))
            elif isinstance(is_successfully_created, Exception):
                return 'ошибка при создании поста, попробуйте ещё раз'
        return 'не введён заголовок или содержание статьи'
    return render_template('create.html')

def post_page(post_id):
    target_post = PostAccess.get_record_by_id(Post, post_id)
    if target_post == None:
        abort(404)
    elif request.method == 'POST':
        if current_user.is_authenticated:
            form_type = request.form.get('form_type')
            if form_type == 'like_post':
                post_author = PostAccess.get_record_by_id(Account, target_post.author_id)
                current_user.following_to.append(post_author)
                print(current_user.following_to)
                print(post_author.followers)
                PostAccess.like_post(post_id, current_user)
            elif form_type == 'write_comment':
                comment_content = request.form['comment_content']
                if comment_content:
                    CommentAccess.create_comment(comment_content, current_user.id, target_post)
            elif form_type == 'like_comment':
                liked_comment_id = request.form['liked_comment_id']
                CommentAccess.like_comment(liked_comment_id, current_user)
    return render_template('post_extended.html', post=target_post)