from rest_framework import serializers

from cooking_core.accounts.serializers.account import AccountSerializer

from ..models.recipe import Recipe


class RecipeReadSerializer(serializers.ModelSerializer):
    creator = AccountSerializer()

    class Meta:
        model = Recipe
        fields = '__all__'
        read_only_fields = ('balance', 'creator')


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
