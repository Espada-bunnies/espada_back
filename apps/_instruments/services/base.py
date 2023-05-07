from django.db.models import Count, Q
from mptt.querysets import TreeQuerySet


class Service:
    def __init__(self, main_queryset):
        self.main_queryset = main_queryset


class PublicationService(Service):

    def __init__(self, image_queryset, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image_queryset = image_queryset

    def get_update_queryset(self, queryset: TreeQuerySet) -> TreeQuerySet:
        update_queryset = queryset.annotate(
            likes_count=Count('ratings', filter=Q(ratings__positive=True)),
            dislikes_count=Count('ratings', filter=Q(ratings__positive=False)),
            sharing_count=Count('sharing'),
        ).order_by('-created_at')
        return update_queryset

    def create(self, validated_data):
        upload_images = validated_data.get('upload_images')
        if upload_images:
            del validated_data['upload_images']
        obj = self.main_queryset.objects.create(**validated_data)
        if upload_images:
            for image in upload_images:
                self.image_queryset.objects.create(relation=obj, image=image)
        return obj


class ActionService(PublicationService):
    def __init__(self, rating_queryset, sharing_queryset, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rating_queryset = rating_queryset
        self.sharing_queryset = sharing_queryset

    def logic_for_like_dislike_or_sharing(self, request, *args, **kwargs):
        action = kwargs.get('action')
        obj_id = kwargs.get('pk')
        user_id = request.user.id or 1
        obj = self._get_or_none(self.rating_queryset, relation=obj_id, rated_user=user_id)
        if action == 'sharing':
            self.sharing_queryset.objects.create(relation_id=obj_id, shared_user_id=user_id)
        elif action == 'like':
            if self._check_already_exists(obj):
                pass
            else:
                self.rating_queryset.objects.create(relation_id=obj_id, rated_user_id=user_id, positive=False)
        elif action == 'dislike':
            if self._check_already_exists(obj, is_like=False):
                pass
            else:
                self.rating_queryset.objects.create(relation_id=obj_id, rated_user_id=user_id, positive=False)

    @staticmethod
    def _get_or_none(queryset, **kwargs):
        try:
            return queryset.objects.get(**kwargs)
        except queryset.DoesNotExist:
            return None

    @staticmethod
    def _check_already_exists(obj, is_like=True) -> bool:
        if obj and obj.positive == is_like:
            obj.delete()
            return True
        elif obj and obj.positive != is_like:
            obj.positive = is_like
            obj.save()
            return True
        return False
