import django_filters


class RecipeFilter(django_filters.FilterSet):
    search = django_filters.BaseCSVFilter(
        field_name='tags__slug',
        method='filter_tags'
    )

    def filter_tags(self, queryset, field_name, values):
        if not values[0] == 'None':
            for value in values:
                queryset = queryset.filter(tags__slug=value)
        return queryset


class FavoriteFilter(django_filters.FilterSet):
    search = django_filters.BaseCSVFilter(
        field_name='recipe__tags__slug',
        method='filter_tags'
    )

    def filter_tags(self, queryset, field_name, values):
        if not values[0] == 'None':
            for value in values:
                queryset = queryset.filter(recipe__tags__slug=value)
        return queryset
