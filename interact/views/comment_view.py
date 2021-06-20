from functools import cached_property

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from django.shortcuts import get_object_or_404

from interact.models import Comment
from interact.serializers.comment_serializer import (
    CommentSerializer,
    CommentObjectSerializer,
    CommentListSerializer,
)
from interact.pagination import CommentLimitOffsetPagination
from interact.permissions import comment_permisssions
from interact.exception import PostNotFound, RefCommentNotFound, CannotRefSubComment
from interact.constants import NUMBER_OF_SUB_COMMENT

from post.models import Post


class CommentView(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = (CommentLimitOffsetPagination)

    @cached_property
    def get_post(self):
        return get_object_or_404(Post, id=self.kwargs['post_id'])

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return self.queryset.filter(post_parent=post_id)

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
            else:  # Add subcomment to comment's latest reply ids string
                new_subcomment = serializer.save()
                ref_comment_latest_reply_ids_string = ref_comment.latest_reply_ids_string
                ids = ref_comment_latest_reply_ids_string.split(';')
                ids.append(str(new_subcomment.id))
                ids = ids[-NUMBER_OF_SUB_COMMENT:]
                ref_comment.latest_reply_ids_string = ids.join(';')
        serializer.save()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        sub_comment_ids = [i.latest_reply_ids_string.split(';') for i in page if i.latest_reply_ids_string != '']
        sub_comment_ids = [int(i) for sub_list in sub_comment_ids for i in sub_list]
        # My implement to get 3 latest reply of each Comment
        sub_comments = Comment.objects.filter(
            id__in=sub_comment_ids
        ).select_related('owner').order_by('-timestamp')
        for comment in page:
            comment.sub_comments = [sub_comment for sub_comment in sub_comments if sub_comment.comment_ref == comment]
        serializer = self.get_serializer(page, many=True)

        return self.get_paginated_response(serializer.data)


class CommentObjectView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentObjectSerializer
    lookup_url_kwarg = 'pk'
    http_method_names = ['patch', 'delete', 'get', 'put']
    permission_classes = [
        comment_permisssions.JustOwnerCanModifyComment,
        IsAuthenticatedOrReadOnly
    ]

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return self.queryset.filter(post_parent=post_id)
