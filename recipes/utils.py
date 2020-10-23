from users.models import Favorite


def get_ingredients(request):
    ingredients = {}
    for key in request.POST:
        if key.startswith('nameIngredient'):
            value_ingredient = key[15:]
            ingredients[request.POST[key]] = request.POST['valueIngredient_' + value_ingredient]
    return ingredients


def get_favorites(request):
    favorites_list = []
    if request.user.is_authenticated:

        favorites_list = list(Favorite.objects.filter(
            user=request.user
        ).values_list('recipe_id', flat=True))

    print(favorites_list)
    return favorites_list
