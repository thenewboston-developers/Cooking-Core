from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=365),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    'SIGNING_KEY': '4fcb9436a426e5d8e215220cfd6cfdbb8c3066111b6eae62cdee57867fadbbd4',
    'UPDATE_LAST_LOGIN': True,
    'USER_ID_FIELD': 'account_number',
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ('rest_framework_simplejwt.authentication.JWTAuthentication',),
    'DEFAULT_PARSER_CLASSES': ('rest_framework.parsers.JSONParser',),
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
}
