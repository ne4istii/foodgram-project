from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from recipes.models import Recipe


class FoodgramModelViewSet(ModelViewSet):

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
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'success': True})
