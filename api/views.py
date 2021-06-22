from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .generics import FoodgramModelViewSet
from recipes.models import Favorite, Ingredient, Purchase, Subscription
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          PurchaseSerializer, SubscriptionSerializer)


User = get_user_model()



class FavoriteViewSet(FoodgramModelViewSet):
    serializer_class = FavoriteSerializer
    queryset = Favorite.objects.all()

    def get_object(self):
        user = self.request.user
        return user.favorites.filter(recipe__id=self.kwargs.get('pk'))


class PurchaseViewSet(FoodgramModelViewSet):
    serializer_class = PurchaseSerializer
    queryset = Purchase.objects.all()

    def get_object(self):
        user = self.request.user
        return user.purchases.filter(recipe__id=self.kwargs.get('pk'))


class IngredientViewSet(FoodgramModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        search_text = self.request.query_params.get('query')
        return queryset.filter(title__istartswith=search_text)


class SubscriptionViewSet(FoodgramModelViewSet):
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()

    def get_object(self):
        author = get_object_or_404(
            User.objects, 
            pk=self.kwargs.get('pk')
        ).id
        return get_object_or_404(
            Subscription.objects, 
            author=author,
            user=self.request.user.pk
        )

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
