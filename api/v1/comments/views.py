from django.http import QueryDict
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps._instruments.permissions import IsAuthorOrReadOnly
from apps.comments.container import comment_service
from apps.comments.models import Comment
from apps.comments.paginate import CommentPaginationPage
from apps.comments.serializers import CommentSerializer


class CommentView(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = (OrderingFilter,)
    ordering_fields = ('created_at', 'likes_count', 'dislikes_count')
    # permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = CommentPaginationPage

    def get_queryset(self):
        post_id = self.kwargs.get('id')
        self.queryset = Comment.objects.filter(post_id=post_id)
        return comment_service.get_update_queryset(self.queryset)

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, QueryDict):
            request.data._mutable = True
        request.data['post'] = kwargs.get('id')
        request.data['user'] = request.user.id or 1
        return super().create(request, *args, **kwargs)


class CommentActionView(CreateAPIView):
    # permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        comment_service.logic_for_like_dislike_or_sharing(request, *args, **kwargs)
        return Response(status=204)
