from functions import write_logs
from models.comment import db, Comment
from repository.ParentAccess import ModelAccess


class CommentAccess(ModelAccess):

    @staticmethod
    def add_comment_to_user_liked_comments(comment, user):
        if comment not in user.liked_comments:
            user.liked_comments.append(comment)
        else:
            user.liked_comments.remove(comment)
        comment.likes = len(user.liked_comments)

    @staticmethod
    @write_logs
    def create_comment(content, author_id, commented_post):
        comment = Comment(content=content, author_id=author_id, post_id = commented_post.id)
        commented_post.comments.append(comment)
        db.session.commit()

    @staticmethod
    @write_logs
    def like_comment(liked_comment_id, user):
        liked_comment = ModelAccess.get_record_by_id(Comment, liked_comment_id)
        CommentAccess.add_comment_to_user_liked_comments(liked_comment, user)
        db.session.commit()