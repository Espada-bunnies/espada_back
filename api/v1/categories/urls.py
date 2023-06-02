from django.urls import path

from api.v1.categories.views import PostAPIViews

urlpatterns = [
    path('list/', PostAPIViews.as_view()),

]

