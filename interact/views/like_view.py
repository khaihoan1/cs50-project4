from functools import cached_property
from rest_framework import viewsets, permissions
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import status
from interact.models import Like
from interact.serializers.like_serializer import LikeSerializer, ListLikeSerializer
from django.shortcuts import get_object_or_404

from interact.permissions import like_permissions
from post.models import Post


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    http_method_names = ['get', 'post', 'delete']
    permission_classes = [like_permissions.JustOwnerCanDelete, permissions.IsAuthenticatedOrReadOnly]

    @cached_property
    def get_post(self):
        return get_object_or_404(Post, id=self.kwargs['post_id'])

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            'post': self.get_post,
        })
        return context

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ListLikeSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        is_like = True if self.kwargs['like_or_dislike'] == 'like' else False
        return self.queryset.filter(post_parent=post_id, is_like=is_like)

    def create(self, request, *args, **kwargs):
        post = self.get_post
        if not post:
            raise NotFound
        if request.user == post.owner:
            return Response({'error': 'You should not like/dislike yourself'})
        elif Like.objects.filter(owner=request.user, post_parent=post):
            return Response({'error': 'You already interact this post'})
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        data_to_return = {
            'like_count_updated': instance.get_count_to_update(
                self.kwargs['like_or_dislike'] == 'like'
            )}  # not just increase like_count by 1, this returns new Like count (by query)
        headers = self.get_success_headers(serializer.data)  # serialize.data cannot be modified
        data_to_return.update(serializer.data)
        return Response(
            data={'inform': "successfully", 'data': data_to_return},
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def perform_create(self, serializer):
        return serializer.save()
