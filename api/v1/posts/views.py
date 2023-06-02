from urllib.request import Request
from django.http import QueryDict
from elasticsearch_dsl import Q
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter

from apps._instruments.permissions import IsAuthorOrReadOnly
from apps.posts.container import post_service
from apps.posts.documents import PostDocument
from apps.posts.models import Post
from apps.posts.serializers import PostSerializer
from apps._instruments.filters.search import SearchPosts



class PostView(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = (SearchPosts,)

    # permission_classes = (IsAuthorOrReadOnly,)

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, QueryDict):
            request.data._mutable = True
        request.data["user"] = request.user.id or 1
        return super().create(request, *args, **kwargs)


class PostActionView(CreateAPIView):
    # permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        post_service.logic_for_like_dislike_or_sharing(request, *args, **kwargs)
        return Response(status=204)





