from interact.models import Comment
from interact.serializers.comment_serializer import (
    CommentSerializer,
    CommentObjectSerializer,
    CommentListSerializer,
)
from interact.permissions import comment_permisssions
from interact.exception import PostNotFoundException, RefCommentNotFound
from rest_framework.mixins import DestroyModelMixin
from rest_framework.generics import ListCreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class CommentListView(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        queryset = self.queryset.filter(post_parent=int(post_id))
        if self.request.method == 'GET':
            queryset = queryset.filter(comment_ref=None).prefetch_related('children_comment')
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CommentListSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        if serializer.validated_data['post_parent'].id != self.kwargs['post_id']:
            raise PostNotFoundException
        if not Comment.objects.filter(
            post_parent__id=self.kwargs['post_id'],
            pk=serializer.validated_data['comment_ref'].pk
        ).exists():
            raise RefCommentNotFound
        serializer.save()


class CommentObjectView(UpdateAPIView, DestroyModelMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentObjectSerializer
    lookup_url_kwarg = 'pk'
    http_method_names = ['patch', 'delete']
    permission_classes = [
        comment_permisssions.JustOwnerCanModifyComment,
    ]
