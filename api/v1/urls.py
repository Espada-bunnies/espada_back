from django.urls import include, path

urlpatterns = [
    path("users/", include("api.v1.users.urls")),
    path("categories/", include("api.v1.categories.urls"))
]
