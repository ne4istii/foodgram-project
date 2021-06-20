from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin, 
                                   ListModelMixin)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from recipes.models import Favorite, Ingredient, Recipe, Purchase, Subscription
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          PurchaseSerializer, SubscriptionSerializer)


User = get_user_model()


class FavoriteViewSet(CreateModelMixin,
                      DestroyModelMixin,
                      GenericViewSet):
    serializer_class = FavoriteSerializer
    queryset = Favorite.objects.all()

    def create(self, request, *args, **kwargs):
        recipe = get_object_or_404(
            Recipe.objects, 
            id=request.data.get('id')
        ).id
        request.data.pop('id')
        request.data.update({
            'user': request.user.id,
            'recipe': recipe,
        })
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        user = request.user
        recipe = user.favorites.filter(recipe__id=kwargs.get('pk'))
        self.perform_destroy(recipe)
        return Response({'success': True})


class IngredientViewSet(ListModelMixin, GenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        search_text = self.request.query_params.get('query')
        return queryset.filter(title__istartswith=search_text)


class SubscriptionViewSet(CreateModelMixin, 
                          DestroyModelMixin,
                          GenericViewSet):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()

    def create(self, request, *args, **kwargs):
        author = get_object_or_404(
            User.objects, 
            id=request.data.get('id')
        ).id
        request.data.pop('id')
        request.data.update({
            'user': request.user.id,
            'author': author,
        })
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        author = get_object_or_404(
            User.objects, 
            pk=kwargs.get('pk')
        ).id
        instance = get_object_or_404(
            Subscription.objects, 
            author=author,
            user=request.user.id
        )
        self.perform_destroy(instance)
        return Response({'success': True})


class PurchaseViewSet(ModelViewSet):
    serializer_class = PurchaseSerializer
    queryset = Purchase.objects.all()

    def create(self, request, *args, **kwargs):
        user = request.user.id
        recipe = get_object_or_404(
            Recipe.objects, 
            id=request.data.get('id')
        ).id
        request.data.pop('id')
        request.data.update({
            'user': user,
            'recipe': recipe,
        })
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        user = request.user
        recipe = user.purchases.filter(recipe__id=kwargs.get('pk'))
        self.perform_destroy(recipe)
        return Response({'success': True})
