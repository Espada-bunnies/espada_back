from django.http import QueryDict
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.posts.container import post_service
from apps.posts.models import Post
from apps.posts.serializers import PostSerializer


class PostView(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('body', 'user__username')
    ordering_fields = ('created_at', 'likes_count', 'dislikes_count')

    # permission_classes = (IsAuthorOrReadOnly,)

    def get_queryset(self):
        return post_service.get_update_queryset(self.queryset)

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, QueryDict):
            request.data._mutable = True
        request.data['user'] = request.user.id or 1
        return super().create(request, *args, **kwargs)


class PostActionView(CreateAPIView):
    # permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        post_service.logic_for_like_dislike_or_sharing(request, *args, **kwargs)
        return Response(status=204)
