from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ..models.recipe import Recipe


class WithdrawSerializer(serializers.Serializer):
    recipe_id = serializers.IntegerField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def validate(self, attrs):
        attrs = super().validate(attrs)
        recipe_id = attrs['recipe_id']
        request = self.context.get('request')

        try:
            recipe = Recipe.objects.get(id=recipe_id)
        except Recipe.DoesNotExist:
            raise serializers.ValidationError('Recipe with the given ID does not exist.')

        if recipe.balance == 0:
            raise ValidationError('Recipe balance is 0')

        if recipe.creator != request.user:
            raise ValidationError('You do not have permission to withdraw from that recipe')

        return recipe
