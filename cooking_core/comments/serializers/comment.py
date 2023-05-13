from rest_framework import serializers

from cooking_core.accounts.serializers.account import AccountSerializer

from ..models.comment import Comment


class CommentReadSerializer(serializers.ModelSerializer):
    creator = AccountSerializer()

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('creator',)


class CommentWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'
