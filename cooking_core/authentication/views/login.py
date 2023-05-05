from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from cooking_core.accounts.serializers.account import AccountSerializer

from ..serializers.login import LoginSerializer


class LoginView(APIView):

    @staticmethod
    def post(request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        account = serializer.save()
        refresh_token = RefreshToken.for_user(account)

        # TODO: Need to return account number as well
        return Response({
            'account': AccountSerializer(account).data,
            'authentication': {
                'access_token': str(refresh_token.access_token),
                'refresh_token': str(refresh_token)
            },
        },)
