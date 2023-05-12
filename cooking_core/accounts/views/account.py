from rest_framework import status, viewsets
from rest_framework.response import Response

from cooking_core.general.permissions import IsAccountOwner
from cooking_core.general.utils.cryptography import generate_key_pair

from ..models import Account
from ..serializers.account import AccountSerializer


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def create(self, request, *args, **kwargs):
        key_pair = generate_key_pair()
        account = Account.objects.create(account_number=key_pair.public)

        results = {
            'account': AccountSerializer(account).data,
            'signing_key': key_pair.private,
        }

        return Response(results, status=status.HTTP_201_CREATED)

    def get_permissions(self):
        if self.action == 'partial_update':
            permission_classes = [IsAccountOwner]
        else:
            permission_classes = []

        return [permission() for permission in permission_classes]
