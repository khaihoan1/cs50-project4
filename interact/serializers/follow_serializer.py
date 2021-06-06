from rest_framework import serializers
from interact.models import Follow


class FollowSerializer(serializers.ModelSerializer):
    # followed_id = serializers.IntegerField(source="followed")
    # follower_id = serializers.IntegerField(source="follower")

    class Meta:
        model = Follow
        fields = '__all__'
        # fields = ('follower',)
