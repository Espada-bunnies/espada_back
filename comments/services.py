from comments.models import Comment, CommentImage, CommentReply


class CommentService:

    def create(self, validated_data):
        reply_to = validated_data.get('reply_to')
        upload_images = validated_data.get('upload_images')
        if reply_to:
            del validated_data['reply_to']
        if upload_images:
            del validated_data['upload_images']
        comment = Comment.objects.create(**validated_data)
        if reply_to:
            comment_reply = Comment.objects.get(id=reply_to)
            CommentReply.objects.create(comment=comment, reply_to=comment_reply)
        if upload_images:
            for image in upload_images:
                CommentImage.objects.create(comment=comment, image=image)
        return comment
