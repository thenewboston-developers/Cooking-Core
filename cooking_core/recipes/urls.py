from rest_framework.routers import SimpleRouter

from .views.recipe import RecipeViewSet

router = SimpleRouter(trailing_slash=False)
router.register('recipes', RecipeViewSet)

urlpatterns = router.urls
