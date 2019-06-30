from rest_framework import serializers

from .models import Post
from users.serializers import UserSerializer


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Post

    def to_representation(self, obj):
        data = super().to_representation(obj)
        data['user'] = UserSerializer(obj.user).data

        return data

    def to_internal_value(self, data):
        request = self.context['request']
        check_ownership = self.context.get('check_ownership', False)

        if check_ownership and not Post.objects.filter(
                pk=data['id'], user=request.user):
            raise serializers.ValidationError({
                'non_field_error': 'You are not permitted to edit this post'
            })

        return super().to_internal_value(data)
