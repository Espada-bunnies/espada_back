from django.shortcuts import render
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from posts.container import post_service
from posts.models import Post
from posts.serializer import PostSerializer
from posts.utils import get_upgrade_queryset


class PostView(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return get_upgrade_queryset()

