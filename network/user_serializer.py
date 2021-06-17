from rest_framework.serializers import ModelSerializer
from network.models import User


class UserInfoForInteractionSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'avatar_pic')
