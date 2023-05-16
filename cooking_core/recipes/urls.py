from django.urls import path
from rest_framework.routers import SimpleRouter

from .views.recipe import RecipeViewSet
from .views.withdraw import WithdrawView

router = SimpleRouter(trailing_slash=False)
router.register('recipes', RecipeViewSet)

urlpatterns = [
    path('withdraw', WithdrawView.as_view()),
]

urlpatterns += router.urls
