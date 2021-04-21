from rest_framework import viewsets, permissions
from interact.models import Like
from interact.serializers import LikeSerializer

from interact.permissions import like_permissions


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    http_method_names = ['get', 'post', 'delete']
    authentication_classes = [like_permissions.JustNotOwnerCanLike, permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_id = self.request.query_params.get('postID')
        if post_id:
            return self.queryset.filter(post_parent=post_id)
        return self.queryset
