from django.urls import path, include

urlpatterns = [
    path('posts/<int:id>/', include('api.v1.comments.urls', namespace='comments')),
    path('posts/', include('api.v1.posts.urls', namespace='posts'))
]

