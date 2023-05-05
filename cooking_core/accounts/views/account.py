from rest_framework import status, viewsets
from rest_framework.response import Response

from cooking_core.general.utils.cryptography import generate_key_pair

from ..models import Account
from ..serializers.account import AccountSerializer


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def create(self, request, *args, **kwargs):
        # TODO: Actually create an account
        key_pair = generate_key_pair()
        account = {
            'account_number': key_pair.public,
            'signing_key': key_pair.private,
        }
        return Response(account, status=status.HTTP_201_CREATED)
