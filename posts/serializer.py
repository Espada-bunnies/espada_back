from rest_framework import serializers

from posts.models import PostImage, PostLike, PostDislike, Post, PostShare


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = '__all__'


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = '__all__'


class PostDislikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostDislike
        fields = '__all__'


class PostShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostShare
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    likes = PostLikeSerializer(many=True, required=False)
    likes_count = serializers.IntegerField(read_only=True)
    dislikes = PostDislikeSerializer(many=True, required=False)
    dislikes_count = serializers.IntegerField(read_only=True)
    sharing = PostShareSerializer(many=True, required=False)
    sharing_count = serializers.IntegerField(read_only=True)
    images = PostImageSerializer(many=True, required=False)

    upload_images = serializers.ListSerializer(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True,
        required=False,
    )

    class Meta:
        model = Post
        fields = '__all__'

