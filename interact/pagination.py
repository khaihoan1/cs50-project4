from rest_framework.pagination import LimitOffsetPagination


class CommentLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 5


# class SubCommentLimitOffsetPagination(LimitOffsetPagination):
#     default_limit = 5

#     def get_offset(self, request):
#         offset = super().get_offset(request)
#         return NUMBER_OF_PRELOADED_SUB_COMMENT if not offset else offset
