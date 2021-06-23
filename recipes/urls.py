from django.urls import path

from . import views

urlpatterns = [
    path(
        'favorites/',
        views.favorites,
        name='favorites'
    ),
    path(
        'follow/',
        views.follow,
        name='follow'
    ),
    path(
        'purchases/',
        views.purchases,
        name='purchases'
    ),
    path(
        'purchases/download/',
        views.purchases_download,
        name='purchases_download'
    ),
    path(
        'recipes/create/',
        views.new_recipe,
        name='new_recipe'
    ),
    path(
        'recipes/<slug:slug>/',
        views.recipe_view,
        name='recipe_view'
    ),
    path(
        '<str:username>/',
        views.profile,
        name='profile'
    ),
    path(
        'recipes/<slug:slug>/edit/',
        views.recipe_edit,
        name='recipe_edit'
    ),
    path(
        'recipes/<slug:slug>/delete/',
        views.recipe_delete,
        name='recipe_delete'
    ),
    path('', views.recipes, name='recipes'),
]
