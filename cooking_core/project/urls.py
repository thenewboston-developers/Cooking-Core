from django.contrib import admin
from django.urls import include, path

import cooking_core.accounts.urls
import cooking_core.blocks.urls
import cooking_core.comments.urls
import cooking_core.config.urls
import cooking_core.recipes.urls
from cooking_core.authentication.views.login import LoginView

API_PREFIX = 'api/'

urlpatterns = [
    path('__debug__/', include('debug_toolbar.urls')),
    path('admin/', admin.site.urls),
    path('login', LoginView.as_view(), name='login'),
    path(API_PREFIX, include(cooking_core.accounts.urls)),
    path(API_PREFIX, include(cooking_core.blocks.urls)),
    path(API_PREFIX, include(cooking_core.comments.urls)),
    path(API_PREFIX, include(cooking_core.config.urls)),
    path(API_PREFIX, include(cooking_core.recipes.urls)),
]
