from django import template

register = template.Library()


@register.filter
def has_purchase(recipe, user):
    return user.purchases.filter(recipe=recipe).exists()


@register.filter
def has_favorite(recipe, user):
    return user.favorites.filter(recipe=recipe).exists()


@register.filter
def get_tags(slug, active_tags):
    if not active_tags:
        return slug
    if slug in active_tags:
        active_tags = active_tags.split(',')
        active_tags.remove(slug)
        active_tags = ','.join(active_tags)
        return f'{active_tags}'
    return f'{slug},{active_tags}'
