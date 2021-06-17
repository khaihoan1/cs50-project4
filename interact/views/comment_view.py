from functools import cached_property
from interact.models import Comment
from interact.serializers.comment_serializer import (
    CommentSerializer,
    CommentObjectSerializer,
    CommentListSerializer,
)
from interact.permissions import comment_permisssions
from interact.exception import PostNotFound, RefCommentNotFound, CannotRefSubComment
from post.models import Post
from rest_framework.mixins import DestroyModelMixin
from rest_framework.generics import ListCreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch, OuterRef, Subquery


class CommentView(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @cached_property
    def get_post(self):
        return get_object_or_404(Post, id=self.kwargs['post_id'])

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        # queryset = self.queryset.filter(post_parent=int(post_id))
        sub_comments = Comment.objects.filter(
            comment_ref=OuterRef('id'),
            post_parent=post_id
        ).order_by('-timestamp').values_list('id', flat=True)[:3]
        if self.request.method == 'GET':
            queryset = Comment.objects.filter(comment_ref=None, post_parent=post_id).select_related('owner').\
                prefetch_related(Prefetch('children_comment', queryset=Comment.objects.filter(
                    id__in=Subquery(sub_comments)
                ), to_attr="cmt")).order_by('-timestamp')[:6]
            # prefetch_related(Prefetch('children_comment', queryset=Comment.objects.filter(
            #     id__in=Subquery(sub_comments.values('pk')[:3])
            # )
            # ))
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CommentListSerializer
        return super().get_serializer_class()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            'post_parent': self.get_post
        })
        return context

    def perform_create(self, serializer):
        if not self.get_post:
            raise PostNotFound
        if serializer.validated_data['comment_ref']:
            ref_comment = Comment.objects.filter(
                post_parent__id=self.kwargs['post_id'],
                pk=serializer.validated_data['comment_ref'].pk
            ).first()
            if not ref_comment:
                raise RefCommentNotFound
            elif ref_comment.comment_ref:
                raise CannotRefSubComment
        serializer.save()


class CommentObjectView(UpdateAPIView, DestroyModelMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentObjectSerializer
    lookup_url_kwarg = 'pk'
    http_method_names = ['patch', 'delete']
    permission_classes = [
        comment_permisssions.JustOwnerCanModifyComment,
    ]
