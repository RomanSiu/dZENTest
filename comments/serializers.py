import bleach
from rest_framework import serializers

from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField(read_only=True)

    ALLOWED_TAGS = ['b', 'i', 'u', 'br']

    class Meta:
        model = Comment
        fields = [
            'id', 'homepage', 'text', 'created_at', 'updated_at',
            'parent', 'replies', 'username', 'email'
        ]
        read_only_fields = ['created_at', 'replies', 'username', 'email']

    def get_replies(self, obj):
        children = obj.replies.all().order_by('-created_at')
        return CommentSerializer(children, many=True, context=self.context).data

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user

        cleaned_text = bleach.clean(validated_data['text'], tags=self.ALLOWED_TAGS, strip=True)

        comment = Comment(
            user=user,
            username=user.username,
            email=user.email,
            homepage=validated_data.get('homepage'),
            text=cleaned_text,
            parent=validated_data.get('parent')
        )
        comment.save()
        return comment
