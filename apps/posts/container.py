from apps._instruments.services.services import PostService
from apps.posts.models import Post, PostImage, PostRating, PostSharing

post_service = PostService(
    main_queryset=Post,
    image_queryset=PostImage,
    rating_queryset=PostRating,
    sharing_queryset=PostSharing,
)
