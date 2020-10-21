from django.shortcuts import redirect
from recipes.models import Recipe


def recipe_remove(request, username, recipe_id):
    if request.user.username == username:
        Recipe.objects.filter(id=recipe_id).delete()
        return redirect("user_recipe_view_page", username)
    else:
        return redirect("recipe_view_page", username, recipe_id)