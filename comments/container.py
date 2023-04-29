from comments.models import Comment
from comments.services import CommentService

comment_service = CommentService(Comment.objects)
