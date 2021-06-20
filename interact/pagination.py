from rest_framework.pagination import LimitOffsetPagination


class CommentLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 5
