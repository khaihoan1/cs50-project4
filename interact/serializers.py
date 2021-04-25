from rest_framework import serializers
from .models import Comment, Like


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    post_like_count = serializers.SerializerMethodField('get_like_count')

    def get_like_count(self, obj):
        return Like.objects.filter(post_parent=obj.post_parent).count()
        # print(self.obj)

    class Meta:
        model = Like
        fields = '__all__'

    def save(self):
        super().save(owner=self.context['request'].user)


class ListLikeSerializer(LikeSerializer):
    def get_like_count(self):
        return Like.objects.filter(post_parent=self.validated_data['post_parent'].count())
    post_like_count = serializers.ModelField('get_like_count')
