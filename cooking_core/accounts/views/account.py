from rest_framework import viewsets

from ..models import Account
from ..serializers.account import AccountSerializer


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
