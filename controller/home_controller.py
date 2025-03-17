from flask import request, render_template
from flask_login import current_user
from models import Post
from repository import PostAccess


def home_page():
    posts = PostAccess.get_all_records(Post)
    if request.method == 'POST':
        if current_user.is_authenticated:
            form_type = request.form['form_type']
            if form_type == 'like_post':
                liked_post_id = request.form['liked_post_id']
                PostAccess.like_post(liked_post_id, current_user)
    return render_template('home.html', posts=posts)

