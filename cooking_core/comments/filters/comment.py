import django_filters

from ..models import Comment


class CommentFilter(django_filters.FilterSet):
    recipe = django_filters.NumberFilter(field_name='recipe', lookup_expr='exact')

    class Meta:
        model = Comment
        fields = ['recipe']
