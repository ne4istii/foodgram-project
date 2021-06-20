from django.urls import include, path

from rest_framework import routers

from .views import (FavoriteViewSet, IngredientViewSet, 
                    PurchaseViewSet, SubscriptionViewSet)


router = routers.DefaultRouter()
router.register(r'favorites', FavoriteViewSet, basename='favorites')
router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register(r'purchases', PurchaseViewSet, basename='purchases')
router.register(r'subscriptions', SubscriptionViewSet, basename='subscriptions')


urlpatterns = [
    path('v1/', include(router.urls)),
]
