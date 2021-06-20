from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import Ingredient, Recipe, Tag, Subscription, Purchase, Favorite

User = get_user_model()


class IngredientRecipeInLine(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1
    verbose_name = 'Ингредиент'
    verbose_name_plural = 'Ингредиенты'


class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientRecipeInLine,)
    list_display = ('slug', 'title', 'author', 'cooking_time', 'get_tags')
    search_fields = ('slug', 'title', 'author', 'cooking_time',)
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


class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональные данные', 
            {'fields': ('first_name', 'last_name', 'email')}
        ),
        ('Разрешения', {'fields': ('is_staff', 'is_active')}),
    )
    list_display = ('username', 'email', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    list_filter = ('username', 'email')
    ordering = ('username', 'email')
    empty_value_display = '-пусто-'


admin.site.unregister(User)
admin.site.unregister(Group)

admin.site.register(User, MyUserAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Purchase)
admin.site.register(Favorite)
admin.site.register(Ingredient)
admin.site.register(Subscription)
admin.site.register(Recipe, RecipeAdmin)
