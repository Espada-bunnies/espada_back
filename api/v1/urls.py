from django.urls import include, path

urlpatterns = [
    path("users/", include("api.v1.users.urls")),
    path("posts/<int:id>/", include("api.v1.comments.urls", namespace="comments")),
    path("posts/<slug:category>/", include("api.v1.posts.urls", namespace="posts")),
]
