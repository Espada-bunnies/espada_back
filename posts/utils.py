from django.db.models import Count

from posts.models import Post


def get_upgrade_queryset():
    queryset = Post.objects.all()
    new_q = Post.objects.annotate(
        likes_count=Count('likes'),
        dislikes_count=Count('dislikes'),
        sharing_count=Count('sharing')
    )
    return new_q
