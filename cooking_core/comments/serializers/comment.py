from rest_framework import serializers

from cooking_core.accounts.serializers.account import AccountSerializer

from ..models.comment import Comment


class CommentReadSerializer(serializers.ModelSerializer):
    creator = AccountSerializer()

    class Meta:
        model = Comment
        fields = '__all__'


class CommentUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('balance', 'creator', 'recipe')


class CommentWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('creator',)

    def create(self, validated_data):
        request = self.context.get('request')
        recipe = super().create({
            **validated_data,
            'creator': request.user,
        })
        return recipe
