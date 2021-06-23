from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import Favorite, Ingredient, Purchase, Recipe, Subscription


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = ('user', 'recipe')
        validators = (
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=('user', 'recipe'),
                message='Такой рецепт уже добавлен!'
            ),
        )


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        exclude = ('id',)


class RecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        exclude = ('id',)


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = ('user', 'author')
        validators = (
            UniqueTogetherValidator(
                queryset=Subscription.objects.all(),
                fields=('user', 'author'),
                message='Такая подписка уже существует!'
            ),
        )


class PurchaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Purchase
        fields = ('user', 'recipe')
        validators = (
            UniqueTogetherValidator(
                queryset=Purchase.objects.all(),
                fields=('user', 'recipe'),
                message='Такой рецепт уже добавлен!'
            ),
        )
