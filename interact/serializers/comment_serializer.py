from rest_framework.serializers import ModelSerializer
from interact.models import Comment
from network.user_serializer import UserInfoForInteractionSerializer


class CommentSerializer(ModelSerializer):  # this serializer is used for creating
    class Meta:
        model = Comment
        fields = ('content', 'comment_ref')

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        validated_data['post_parent'] = self.context['post_parent']
        return self.Meta.model.objects.create(**validated_data)


class CommentObjectSerializer(ModelSerializer):  # this one is used for modifying/deleting
    class Meta:
        model = Comment
        fields = ('content',)


class ChildCommentSerializer(ModelSerializer):  # serializer for child comments in list
    owner = UserInfoForInteractionSerializer()

    class Meta:
        model = Comment
        fields = ('content', 'timestamp', 'owner', 'id')


class CommentListSerializer(ModelSerializer):  # this one is used for listing comments
    children_comment = ChildCommentSerializer(many=True, source='sub_comments')
    owner = UserInfoForInteractionSerializer()

    class Meta:
        model = Comment
        fields = ('id', 'content', 'timestamp', 'owner', 'post_parent', 'children_comment')
