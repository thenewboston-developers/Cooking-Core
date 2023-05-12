from rest_framework import status, viewsets
from rest_framework.response import Response

from cooking_core.general.permissions import IsObjectCreatorOrReadOnly

from ..models import Recipe
from ..serializers.recipe import RecipeSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsObjectCreatorOrReadOnly]
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data={
            **request.data,
            'creator': request.user.pk,
        })
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
