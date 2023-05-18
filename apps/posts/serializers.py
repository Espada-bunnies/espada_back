import datetime

from rest_framework import serializers

from apps._instruments.validators.validators import (BodyValidator,
                                                     ImagesValidator)
from apps.posts.container import post_service
from apps.posts.models import Post, PostImage


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(read_only=True)
    dislikes_count = serializers.IntegerField(read_only=True)
    sharing_count = serializers.IntegerField(read_only=True)
    images = PostImageSerializer(many=True, required=False)
    upload_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True,
        required=False,
        validators=(ImagesValidator(),),
    )
    body = serializers.CharField(validators=(BodyValidator(),))

    class Meta:
        model = Post
        fields = "__all__"

    def create(self, validated_data):
        return post_service.create(validated_data)

    def update(self, instance, validated_data):
        instance.updated_at = datetime.datetime.now()
        return super().update(instance, validated_data)
