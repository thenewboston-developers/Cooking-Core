from rest_framework import serializers

from cooking_core.accounts.serializers.account import AccountSerializer
from cooking_core.general.balance import validate_balance_covers_transaction_fee

from ..models.recipe import Recipe


class RecipeReadSerializer(serializers.ModelSerializer):
    creator = AccountSerializer()

    class Meta:
        model = Recipe
        fields = '__all__'


class RecipeWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = '__all__'
        read_only_fields = ('balance', 'creator')

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
        validate_balance_covers_transaction_fee(account_number=request.user.pk)
        return attrs
