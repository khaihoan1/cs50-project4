from rest_framework import viewsets, permissions
from rest_framework.response import Response
from interact.models import Like
from interact.serializers import LikeSerializer

from interact.permissions import like_permissions
from post.models import Post


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    http_method_names = ['get', 'post', 'delete']
    permission_classes = [like_permissions.JustOwnerCanDelete, permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_id = self.request.query_params.get('post_id')
        if post_id:
            return self.queryset.filter(post_parent=post_id)
        return self.queryset

    def create(self, request):
        post = Post.objects.get(id=request.data['post_parent'])
        if request.user == post.owner:
            return Response({'error': 'You should not like/dislike yourself'})
        elif Like.objects.filter(owner=request.user, post_parent=post):
            return Response({'error': 'You already interact this post'})
        return super().create(request)

    def list(self, request):
        post_id = request.query_params.get('post_id')
        if not post_id:
            return Response({'error': 'You must give a post to get its likes info'})
        return super().list(request)
