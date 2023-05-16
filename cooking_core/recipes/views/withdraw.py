from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cooking_core.accounts.models import Account

from ..serializers.withdraw import WithdrawSerializer


class WithdrawView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        serializer = WithdrawSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        recipe = serializer.validated_data

        # It is crucial to make select_for_update(), so we get database row lock till the moment of actual update
        account = Account.objects.select_for_update().get_or_none(account_number=request.user.pk)
        account.balance += recipe.balance
        account.save()

        recipe.balance = 0
        recipe.save()

        return Response(data={}, status=status.HTTP_200_OK)
