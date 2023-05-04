from django.contrib import admin
from django.urls import include, path

import cooking_core.accounts.urls

API_PREFIX = 'api/'

urlpatterns = [
    path('admin/', admin.site.urls),
    path(API_PREFIX, include(cooking_core.accounts.urls)),
]
