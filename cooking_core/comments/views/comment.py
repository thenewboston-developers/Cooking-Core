from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.response import Response

from cooking_core.general.permissions import IsObjectCreatorOrReadOnly

from ..filters.comment import CommentFilter
from ..models import Comment
from ..serializers.comment import CommentReadSerializer, CommentWriteSerializer


class CommentViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_class = CommentFilter
    permission_classes = [IsObjectCreatorOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentWriteSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data={
            **request.data,
            'creator': request.user.pk,
        })
        serializer.is_valid(raise_exception=True)
        comment = serializer.save()
        read_serializer = CommentReadSerializer(comment)

        return Response(read_serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        return Comment.objects.order_by('-modified_date')

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update', 'update']:
            return CommentWriteSerializer

        return CommentReadSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        comment = serializer.save()
        read_serializer = CommentReadSerializer(comment)

        return Response(read_serializer.data)
