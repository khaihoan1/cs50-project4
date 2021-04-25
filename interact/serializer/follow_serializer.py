from rest_framework.serializers import ModelSerializer
from interact.models import Follow


class FollowSerializer(ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'
