from rest_framework import serializers

from .models import Post
from users.serializers import UserSerializer


class PostSerializer(serializers.ModelSerializer):
    stats = serializers.SerializerMethodField(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'content',
            'created_at',
            'last_edited',
            'user',
            'stats',
        )

    def get_stats(self, obj):
        return {
            'score': obj.score,
            'likes': obj.likes,
            'dislikes': obj.dislikes,
        }

