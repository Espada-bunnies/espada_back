from django.db.models import F

from comments.models import Comment, CommentLike, CommentDislike
from comments.serializers import CommentSerializer


def get_list_data():
    serializer = CommentSerializer(Comment.objects.all(), many=True)
    for row in serializer.data:
        attrs = Comment.objects.select_related('commentreply__reply_to').filter(
            commentreply__reply_to=row.get('id')).all()
        ser = CommentSerializer(attrs, many=True)
        row['replies'] = ser.data
    return serializer


def create_req_data_for_comment_view(request, *args, **kwargs):
    request.data['post'] = kwargs.get('id')
    request.data['user'] = request.user.id or 1
    return request


def add_or_remove_like(request, *args, **kwargs):
    comment_id = kwargs.get('pk')
    user_id = request.user.id or 1
    obj = CommentLike.objects.filter(user_liking=user_id, comment=comment_id)
    obj2 = CommentDislike.objects.filter(user_disliking=user_id, comment=comment_id)
    if obj.exists():
        obj.delete()
        Comment.objects.filter(id=comment_id).update(likes_count=F('likes_count') - 1)
        return None
    elif obj2.exists():
        obj2.delete()
        Comment.objects.filter(id=comment_id).update(dislikes_count=F('dislikes_count') - 1)
        Comment.objects.filter(id=comment_id).update(likes_count=F('likes_count') + 1)
        request.data['comment'] = comment_id
        request.data['user_liking'] = user_id
        return request
    else:
        Comment.objects.filter(id=comment_id).update(likes_count=F('likes_count') + 1)
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
        Comment.objects.filter(id=comment_id).update(dislikes_count=F('dislikes_count') - 1)
        return None
    elif obj2.exists():
        obj2.delete()
        Comment.objects.filter(id=comment_id).update(likes_count=F('likes_count') - 1)
        Comment.objects.filter(id=comment_id).update(dislikes_count=F('dislikes_count') + 1)
        request.data['comment'] = comment_id
        request.data['user_disliking'] = user_id
        return request
    else:
        Comment.objects.filter(id=comment_id).update(dislikes_count=F('dislikes_count') + 1)
        request.data['comment'] = comment_id
        request.data['user_disliking'] = user_id
        return request


