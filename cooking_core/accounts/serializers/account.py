from rest_framework import serializers

from ..models.account import Account


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ('account_number', 'balance', 'display_image', 'display_name')
        read_only_fields = ('account_number', 'balance')
