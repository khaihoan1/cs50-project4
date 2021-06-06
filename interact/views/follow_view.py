from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from interact.models import Follow
from interact.serializers.follow_serializer import FollowSerializer
from rest_framework.response import Response
from django.db import IntegrityError


class FollowListView(ModelViewSet):
    http_method_names = ['get', 'post', 'delete']
    serializer_class = FollowSerializer

    def create(self, request, *args, **kwargs):
        followed = request.data.get('followed')
        if request.user.id != int(request.data.get('follower')):
            return Response({
                'error': 'Don\'t help anyone follow people'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if request.user.id == int(followed):
            return Response({'error': 'You should not follow yourself like a psycho'})
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError:
            return Response({'error': 'Follower already followed the followed'})

    def get_queryset(self):
        # return Follow.objects.filter(followed=self.kwargs['followed_id'])
        return Follow.objects.all()

    def get_object(self):
        return get_object_or_404(Follow, follower=self.request.user, followed=self.request.data['followed'])

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(data={'data': 'Deleted'}, status=status.HTTP_200_OK)
