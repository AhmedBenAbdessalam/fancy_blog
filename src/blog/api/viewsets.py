from posts.models import Post
from rest_framework import viewsets
from .serializers import PostSerializer

# Project viewset
# allows us to create a CRUD api without specifying methods for functionality


class PostViewSet(viewsets.ModelViewSet):

    queryset = Post.objects.all()
    serializer_class = PostSerializer
