from rest_framework.serializers import ModelSerializer
from interact.models import Comment
from network.user_serializer import UserInfoForInteractionSerializer


class CommentSerializer(ModelSerializer):  # this serializer is used for creating
    class Meta:
        model = Comment
        fields = ('content', 'post_parent', 'comment_ref')

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        # validated_data['comment_ref'] =
        return self.Meta.model.objects.create(**validated_data)
        # return 'gg'


class CommentObjectSerializer(ModelSerializer):  # this one is used for modifying/deleting
    class Meta:
        model = Comment
        fields = ('content')


class ChildCommentSerializer(ModelSerializer):  # serializer for child comments in list
    class Meta:
        model = Comment
        fields = ('content', 'timestamp', 'owner')


class CommentListSerializer(ModelSerializer):  # this one is used for listing comments
    children_comment = ChildCommentSerializer(many=True)
    owner = UserInfoForInteractionSerializer()

    class Meta:
        model = Comment
        fields = ('id', 'content', 'timestamp', 'owner', 'post_parent', 'children_comment')
