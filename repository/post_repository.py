from models import Post, db
from functions import write_logs
from repository.ParentAccess import ModelAccess


class PostAccess(ModelAccess):

    @staticmethod
    @write_logs
    def like_post(post_id, user):
        post = ModelAccess.get_record_by(Post, id=post_id)
        if post not in user.liked_posts:
            user.liked_posts.append(post)
        else:
            user.liked_posts.remove(post)
        post.likes = len(post.liked_by.all())
        db.session.commit()










