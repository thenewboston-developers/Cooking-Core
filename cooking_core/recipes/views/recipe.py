from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from cooking_core.config.models import get_value
from cooking_core.general.balance import deduct_amount
from cooking_core.general.permissions import IsObjectCreatorOrReadOnly

from ..filters.recipe import RecipeFilter
from ..models import Recipe
from ..serializers.recipe import RecipeReadSerializer, RecipeWriteSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsObjectCreatorOrReadOnly]
    queryset = Recipe.objects.all()
    serializer_class = RecipeWriteSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        recipe = serializer.save()
        read_serializer = RecipeReadSerializer(recipe)

        creator = recipe.creator
        transaction_fee = get_value('transaction_fee')
        deduct_amount(account_number=creator.pk, amount=transaction_fee)

        return Response(read_serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        return Recipe.objects.select_related('creator').order_by('-modified_date')

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update', 'update']:
            return RecipeWriteSerializer

        return RecipeReadSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, context={'request': request}, partial=partial)
        serializer.is_valid(raise_exception=True)
        recipe = serializer.save()
        read_serializer = RecipeReadSerializer(recipe)

        creator = recipe.creator
        transaction_fee = get_value('transaction_fee')
        deduct_amount(account_number=creator.pk, amount=transaction_fee)

        return Response(read_serializer.data)
