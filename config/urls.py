from django.contrib import admin
from django.urls import include, path,re_path
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView,
                                   SpectacularSwaggerView)
from api.v1.users.views import test_oauth

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("api.v1.urls")),
    re_path('', include('social_django.urls', namespace='social')),
    re_path("oauthtest/",test_oauth,name='oauth'),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]
