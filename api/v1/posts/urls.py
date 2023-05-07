from django.urls import path
from rest_framework import routers

from api.v1.posts.views import PostView, PostActionView

app_name = 'posts'

router = routers.SimpleRouter()
router.register(r'', PostView)

urlpatterns = [
    path('comments/<slug:action>/<int:pk>/', PostActionView.as_view(), name='action')
]

urlpatterns += router.urls
