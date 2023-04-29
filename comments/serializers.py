from rest_framework import serializers

from comments.container import comment_service
from comments.models import Comment, CommentLike, CommentImage, CommentDislike
from comments.validators import CommentBodyValidator, CommentImagesValidator


class CommentImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentImage
        fields = '__all__'


class CommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentLike
        fields = '__all__'


class CommentDislikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentDislike
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    likes = CommentLikeSerializer(many=True, required=False)
    dislikes = CommentDislikeSerializer(many=True, required=False)
    images = CommentImageSerializer(many=True, required=False)
    reply_to = serializers.IntegerField(write_only=True, required=False)
    upload_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True,
        required=False,
        validators=(CommentImagesValidator(),)
    )
    body = serializers.CharField(validators=(CommentBodyValidator(),))

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        return comment_service.create(validated_data)

    def update(self, instance, validated_data):
        instance.updated = True
        return super().update(instance, validated_data)
