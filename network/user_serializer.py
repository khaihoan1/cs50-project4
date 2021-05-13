from rest_framework.serializers import ModelSerializer
from network.models import User


class UserInfoForInteraction(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')
