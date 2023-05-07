from django.urls import path
from rest_framework import routers

from api.v1.comments.views import CommentView, CommentActionView

app_name = 'comments'

router = routers.SimpleRouter()
router.register(r'comments', CommentView)


urlpatterns = [
    path('comments/<slug:action>/<int:pk>/', CommentActionView.as_view(), name='action')
]

urlpatterns += router.urls
