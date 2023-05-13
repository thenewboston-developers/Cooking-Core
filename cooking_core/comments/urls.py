from rest_framework.routers import SimpleRouter

from .views.comment import CommentViewSet

router = SimpleRouter(trailing_slash=False)
router.register('comments', CommentViewSet)

urlpatterns = router.urls
