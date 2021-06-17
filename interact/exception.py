from rest_framework.exceptions import APIException
from rest_framework import status


class PostNotFound(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Post not found'


class RefCommentNotFound(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Referenced comment not found'


class CannotRefSubComment(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Cannot reply a reply'
