from django.db.models import Count

from comments.models import Comment, CommentLike, CommentDislike
from comments.serializers import CommentSerializer


def get_update_queryset(queryset):
    new_q = queryset.annotate(
        likes_count=Count('likes'),
        dislikes_count=Count('dislikes'),
    )
    return new_q


def get_list_data(queryset):
    serializer = CommentSerializer(queryset, many=True)
    for row in serializer.data:
        attrs = queryset.select_related('commentreply__reply_to').filter(
            commentreply__reply_to=row.get('id')).all()
        ser = CommentSerializer(attrs, many=True)
        row['replies'] = ser.data
    return serializer


def add_or_remove_like(request, *args, **kwargs):
    comment_id = kwargs.get('pk')
    user_id = request.user.id or 1
    obj = CommentLike.objects.filter(user_liking=user_id, comment=comment_id)
    obj2 = CommentDislike.objects.filter(user_disliking=user_id, comment=comment_id)
    if obj.exists():
        obj.delete()
        return None
    elif obj2.exists():
        obj2.delete()
        request.data['comment'] = comment_id
        request.data['user_liking'] = user_id
        return request
    else:
        request.data['comment'] = comment_id
        request.data['user_liking'] = user_id
        return request


def add_or_remove_dislike(request, *args, **kwargs):
    comment_id = kwargs.get('pk')
    user_id = request.user.id or 1
    obj = CommentDislike.objects.filter(user_disliking=user_id, comment=comment_id)
    obj2 = CommentLike.objects.filter(user_liking=user_id, comment=comment_id)
    if obj.exists():
        obj.delete()
        return None
    elif obj2.exists():
        obj2.delete()
        request.data['comment'] = comment_id
        request.data['user_disliking'] = user_id
        return request
    else:
        request.data['comment'] = comment_id
        request.data['user_disliking'] = user_id
        return request


