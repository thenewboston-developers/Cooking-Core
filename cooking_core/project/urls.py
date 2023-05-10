from django.contrib import admin
from django.urls import include, path

import cooking_core.accounts.urls
import cooking_core.recipes.urls
from cooking_core.authentication.views.login import LoginView

API_PREFIX = 'api/'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login', LoginView.as_view(), name='login'),
    path(API_PREFIX, include(cooking_core.accounts.urls)),
    path(API_PREFIX, include(cooking_core.recipes.urls)),
]
