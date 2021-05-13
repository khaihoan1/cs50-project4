from rest_framework.exceptions import APIException
from rest_framework import status


class PostNotFoundException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Post not found'


class RefCommentNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Referenced comment not found'
