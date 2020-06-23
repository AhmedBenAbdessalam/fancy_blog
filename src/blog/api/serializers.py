from rest_framework import serializers
from posts.models import Post

# project serializer


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
