from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from comments.models import Comment, CommentLike, CommentDislike
from comments.serializers import CommentSerializer, CommentLikeSerializer, CommentDislikeSerializer
from comments.utils import add_or_remove_like, get_list_data, add_or_remove_dislike, get_update_queryset


class CommentView(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = (OrderingFilter,)
    ordering_fields = ('created_at', 'likes_count', 'dislikes_count')
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        post_id = self.kwargs.get('id')
        self.queryset = Comment.objects.filter(post_id=post_id)
        return get_update_queryset(self.queryset)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = get_list_data(queryset)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        request.data._mutable = True
        request.data['post'] = kwargs.get('id')
        request.data['user'] = request.user.id or 1
        return super().create(request, *args, **kwargs)


class CommentLikeView(CreateAPIView):
    queryset = CommentLike.objects.all()
    serializer_class = CommentLikeSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        need_add = add_or_remove_like(request, *args, **kwargs)
        if not need_add:
            return Response(status=204)
        return super().create(request, *args, **kwargs)


class CommentDislikeView(CreateAPIView):
    queryset = CommentDislike.objects.all()
    serializer_class = CommentDislikeSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        need_add = add_or_remove_dislike(request, *args, **kwargs)
        if not need_add:
            return Response(status=204)
        return super().create(request, *args, **kwargs)
