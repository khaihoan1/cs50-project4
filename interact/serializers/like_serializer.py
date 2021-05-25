from rest_framework import serializers
from interact.models import Like
from network.user_serializer import UserInfoForInteractionSerializer


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('is_like',)

    def save(self):
        return super().save(owner=self.context['request'].user, post_parent=self.context['post'])


class ListLikeSerializer(serializers.ModelSerializer):
    owner = UserInfoForInteractionSerializer()

    class Meta:
        fields = ('owner',)
        model = Like


# class LikeInfoReturnedAfterCreate(serializers.ModelSerializer):
#     like_count = serializers.SerializerMethodField('get_like_count')

#     def get_like_count(self, obj):
#         is_like = obj.is_like
#         return Like.objects.filter(post_parent=obj.post_parent, is_like=is_like).count()

#     class Meta:
#         model = Like
