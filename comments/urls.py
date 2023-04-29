from django.urls import path
from rest_framework import routers

from comments.views import CommentView, CommentLikeView, CommentDislikeView

app_name = 'comments'

router = routers.SimpleRouter()
router.register(r'comments', CommentView)


urlpatterns = [
    path('comments/likes/<int:pk>/', CommentLikeView.as_view()),
    path('comments/dislikes/<int:pk>/', CommentDislikeView.as_view())
]

urlpatterns += router.urls
