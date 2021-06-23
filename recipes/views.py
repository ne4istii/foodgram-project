from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import FileResponse
from django.shortcuts import get_object_or_404, redirect, render

from .filters import FavoriteFilter, RecipeFilter
from .forms import RecipeForm
from .models import  Ingredient, IngredientRecipe, Recipe, Tag, User 
from foodgram.settings import OBJ_PER_PAGE
from .utils import get_ingredients, get_purchase_ingredients

import datetime
import io
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


User = get_user_model()


def recipes(request):
    user = request.user
    tags = Tag.objects.all()
    recipes = RecipeFilter(
        request.GET, 
        queryset=Recipe.objects.all()
    )
    active_tags = recipes.data.get('search')
    paginator = Paginator(recipes.qs, OBJ_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    purchases_counter = user.purchases.count()
    return render(request,"index.html", {
        'active_tags': active_tags,
        'tags': tags,
        'page': page,
        'paginator': paginator,
        'purchases_counter': purchases_counter
    })
 

def recipe_view(request, slug):
    recipe = get_object_or_404(
        Recipe.objects, 
        slug=slug
    )
    is_author = recipe.author == request.user
    is_following = recipe.author.following.filter(
        user__id=request.user.id
        ).exists()
    is_purchassing = recipe.purchases.filter(
        user__id=request.user.id
    ).exists()
    ingredientsrecipe = recipe.ingredientsrecipe.all()
    return render(request, 'singlePage.html', {
        'recipe': recipe,
        'is_author': is_author,
        'is_following': is_following,
        'is_purchassing':is_purchassing,
        'ingredientsrecipe': ingredientsrecipe
    }) 


def profile(request, username):
    author = get_object_or_404(
        User, 
        username=username
    )
    tags = Tag.objects.all()
    recipes = RecipeFilter(
        request.GET, 
        queryset=author.recipes.all()
    )
    active_tags = recipes.data.get('search')
    paginator = Paginator(recipes.qs, OBJ_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    is_author = author == request.user
    is_following = author.following.filter(
        user__id=request.user.id
    ).exists()
    return render(request, 'authorRecipe.html', {
        'active_tags': active_tags,
        'tags': tags,
        'page': page, 
        'author': author,
        'paginator': paginator,
        'recipes': recipes,
        'is_author': is_author,
        'is_following': is_following,
    })


def save_recipe(request, form):
    recipe = form.save(commit=False)
    recipe.author = request.user
    recipe.save()
    ingredients = get_ingredients(request)
    # находим ингредиенты для удаления из рецепта
    for ingredient in recipe.ingredients.all():
        if ingredient.title not in ingredients.keys():
            IngredientRecipe.objects.filter(
                recipe=recipe,
                ingredient=ingredient,
        ).delete()
    # ингредиенты из POST запроса для создания и редактирования
    for name, quantity in ingredients.items():
        ingredient = get_object_or_404(Ingredient, title=name)
        IngredientRecipe.objects.update_or_create(
                recipe=recipe,
                ingredient=ingredient,
                defaults={'amount': quantity}
        )
    tags = request.POST.getlist('tags')
    recipe.tags.clear()
    for slug in tags:
        obj = get_object_or_404(Tag, slug=slug)
        obj.recipes.add(recipe)


@login_required
def new_recipe(request):
    if request.method != 'POST':
        form = RecipeForm()
        return render(request, 'formRecipe.html', {
            'form': form,
        })
    form = RecipeForm(
        request.POST or None,
        files=request.FILES or None,
    )
    if form.is_valid():
        save_recipe(request, form)
        return redirect(
            'recipes'
        )
    return render(request, 'formRecipe.html', {
            'form': form,
        })


@login_required
def recipe_edit(request, slug):
    recipe = get_object_or_404(
        Recipe.objects, 
        slug=slug
    )
    is_author = recipe.author == request.user
    form = RecipeForm(
        data=request.POST or None, 
        files=request.FILES or None, 
        instance=recipe
    )
    ingredientsrecipe = recipe.ingredientsrecipe.all()
    if form.is_valid():
        save_recipe(request, form)
        return redirect(
            'recipe_view', 
            recipe.slug,
        )
    return render(request, 'formRecipe.html', {
        'form': form, 
        'recipe': recipe,
        'ingredientsrecipe': ingredientsrecipe,
        'is_author': is_author
    })


@login_required
def recipe_delete(request, slug):
    get_object_or_404(
        Recipe, 
        slug=slug
    ).delete()
    return redirect('recipes')


@login_required
def follow(request):
    user = request.user
    # user_followings - на кого подписан request.user
    user_followings = user.follower.all()
    paginator = Paginator(user_followings, OBJ_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'myFollow.html', {
        'page': page,
        'paginator': paginator,
    })


@login_required
def purchases(request):
    user = request.user
    purchases = user.purchases.all()
    paginator = Paginator(purchases, OBJ_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'shopList.html', {
        'page': page, 
        'paginator': paginator,
    })


@login_required
def favorites(request):
    user = request.user
    tags = Tag.objects.all()
    recipesfavorite = FavoriteFilter(
        request.GET, 
        queryset=user.favorites.all()
    )
    active_tags = recipesfavorite.data.get('search')
    paginator = Paginator(recipesfavorite.qs, OBJ_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'favorite.html', {
        'active_tags': active_tags,
        'tags': tags,
        'page': page,
        'paginator': paginator,
    })


@login_required
def purchases_download(request):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    pdfmetrics.registerFont(TTFont('DejaVuSerif', 'DejaVuSerif.ttf'))
    p.setFont('DejaVuSerif', 14)
    x = 100
    y = 800
    p.drawString(x, y, 'Покупки:')
    data = get_purchase_ingredients(request)
    delta = 20
    counter = 1
    for value in data.values():
        y -= delta
        ingredient, amount, dimension = value.values()
        p.drawString(x, y, f'{counter}. {ingredient} - {amount} {dimension}')
        counter += 1
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(
        buffer, 
        as_attachment=True, 
        filename=f'purchases_{datetime.datetime.now()}.pdf'
    )


def page_not_found(request, exception):
    return render(request, 'misc/404.html', 
        {'path': request.path}, 
        status=404
    )


def server_error(request):
    return render(request, 'misc/500.html', 
        status=500
    )
