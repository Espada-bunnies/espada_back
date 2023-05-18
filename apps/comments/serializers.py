from rest_framework import serializers

from apps._instruments.validators.validators import (BodyValidator,
                                                     ImagesValidator)
from apps.comments.container import comment_service
from apps.comments.models import Comment, CommentImage


class CommentImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentImage
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    images = CommentImageSerializer(many=True, required=False)
    likes_count = serializers.IntegerField(read_only=True)
    dislikes_count = serializers.IntegerField(read_only=True)
    upload_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True,
        required=False,
        validators=(ImagesValidator(),),
    )
    body = serializers.CharField(validators=(BodyValidator(),))

    class Meta:
        model = Comment
        fields = "__all__"

    def create(self, validated_data):
        return comment_service.create(validated_data)

    def update(self, instance, validated_data):
        instance.updated = True
        return super().update(instance, validated_data)
