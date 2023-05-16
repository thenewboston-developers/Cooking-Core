from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.response import Response

from cooking_core.accounts.models.account import Account
from cooking_core.config.models import get_value
from cooking_core.general.permissions import IsObjectCreatorOrReadOnly

from ..filters.comment import CommentFilter
from ..models import Comment
from ..serializers.comment import CommentReadSerializer, CommentUpdateSerializer, CommentWriteSerializer


class CommentViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_class = CommentFilter
    permission_classes = [IsObjectCreatorOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentWriteSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        comment = serializer.save()

        amount = comment.amount
        creator = comment.creator
        recipe = comment.recipe

        transaction_fee = get_value('transaction_fee')
        total_amount = amount + transaction_fee

        # It is crucial to make select_for_update(), so we get database row lock till the moment of actual update
        sender = Account.objects.select_for_update().get_or_none(account_number=creator.pk)
        sender.balance -= total_amount
        assert sender.balance >= 0
        sender.save()

        recipe.balance += amount
        recipe.save()

        read_serializer = CommentReadSerializer(comment)

        return Response(read_serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        return Comment.objects.order_by('-modified_date')

    def get_serializer_class(self):
        if self.action == 'create':
            return CommentWriteSerializer

        if self.action in ['partial_update', 'update']:
            return CommentUpdateSerializer

        return CommentReadSerializer

    def update(self, request, *args, **kwargs):
        # TODO: Take a fee
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        comment = serializer.save()
        read_serializer = CommentReadSerializer(comment)

        return Response(read_serializer.data)
