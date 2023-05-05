from django.contrib.auth import get_user_model
from rest_framework import serializers

from cooking_core.core.constants import ACCOUNT_NUMBER_LENGTH
from cooking_core.core.utils.cryptography import derive_public_key

Account = get_user_model()


class LoginSerializer(serializers.Serializer):
    signing_key = serializers.CharField(max_length=ACCOUNT_NUMBER_LENGTH)

    def create(self, validated_data):
        return validated_data['account']

    def update(self, instance, validated_data):
        pass

    def validate(self, data):
        signing_key = data['signing_key'].lower().strip()
        public_key = derive_public_key(signing_key)
        account = Account.objects.get(account_number=public_key)

        if not account:
            raise serializers.ValidationError('Invalid login credentials')

        return {'account': account}
