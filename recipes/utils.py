from decimal import Decimal


def get_ingredients(request):
    ingredients = {}
    post = request.POST
    for key, name in post.items():
        if key.startswith('nameIngredient'):
            num = key.partition('_')[-1]
            ingredients.update({
                name: Decimal(post[f'valueIngredient_{num}'].replace(',', '.'))
            })
    return ingredients


def get_purchase_ingredients(request):
    user = request.user
    purchases = user.purchases.all()
    data = {}
    for purchase in purchases:
        ingredients_recipe = purchase.recipe.ingredientsrecipe.all()
        for ir in ingredients_recipe:
            if ir.ingredient.id in data.keys():
                data[ir.ingredient.id]['amount'] += ir.amount
            else:
                data.update({ir.ingredient.id: {
                    'ingredient': ir.ingredient.title,
                    'amount': ir.amount,
                    'dimension': ir.ingredient.dimension
                }})
    return data
