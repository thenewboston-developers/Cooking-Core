from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from cooking_core.accounts.models.account import Account
from cooking_core.accounts.serializers.account import AccountSerializer
from cooking_core.config.models import get_value

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
        read_only_fields = ('amount', 'creator', 'recipe')


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

    def validate(self, attrs):
        attrs = super().validate(attrs)
        request = self.context.get('request')

        # It is crucial to make select_for_update(), so we get database row lock till the moment of actual update
        sender_account = Account.objects.select_for_update().get_or_none(account_number=request.user.pk)
        if sender_account is None:
            raise ValidationError({'sender': ['Sender account does not exist']})

        total_amount = attrs['amount'] + get_value('transaction_fee')

        if sender_account.balance < total_amount:
            raise ValidationError({'amount': ['Total amount is greater than senders account balance']})

        return attrs
