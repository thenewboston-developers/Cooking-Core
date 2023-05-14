from django.urls import re_path

from cooking_core.accounts.consumers import AccountConsumer

websocket_urlpatterns = [
    re_path(r'ws/accounts/(?P<account_number>[a-f0-9]{64})$', AccountConsumer.as_asgi()),
]
