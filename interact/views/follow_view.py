from interact.models import Follow
from interact.serializers.follow_serializer import FollowSerializer
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from django.db import IntegrityError


class FollowListView(ListCreateAPIView):
    http_method_names = ['get', 'post', 'delete']
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    def create(self, request, *args, **kwargs):
        followed_id = request.data.get('followed')
        if request.user.id == int(followed_id):
            return Response({'error': 'You should not follow yourself like a psycho'})
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError:
            return Response({'error': 'Follower already followed the followed'})
