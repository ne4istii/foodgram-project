from django.contrib import admin

from .models import Ingredient, Recipe, Tag, Subscription, Purchase, Favorite


class IngredientRecipeInLine(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1
    verbose_name = 'Ингредиент'
    verbose_name_plural = 'Ингредиенты'


class IngredientAdmin(admin.ModelAdmin):
    search_fields = ('title',)


class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientRecipeInLine,)
    list_display = ('slug', 'title', 'author', 'cooking_time', 'get_tags')
    search_fields = ('title',)
    list_filter = ('author', 'cooking_time', 'tags')
    ordering = ('-pub_date',)
    empty_value_display = '-пусто-'
    prepopulated_fields = {'slug': ('title',)}

    def get_tags(self, obj):
        qs = obj.list_tags()
        if qs:
            return list(qs)

    get_tags.short_description = 'Теги'


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    list_filter = ('name', 'slug')
    empty_value_display = '-пусто-'
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Tag, TagAdmin)
admin.site.register(Purchase)
admin.site.register(Favorite)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Subscription)
admin.site.register(Recipe, RecipeAdmin)
