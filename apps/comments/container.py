from apps._instruments.services.services import CommentService
from apps.comments.models import (Comment, CommentImage, CommentRating,
                                  CommentSharing)

comment_service = CommentService(
    main_queryset=Comment,
    image_queryset=CommentImage,
    rating_queryset=CommentRating,
    sharing_queryset=CommentSharing,
)
