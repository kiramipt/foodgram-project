from django.shortcuts import render, redirect, get_object_or_404
from .models import Recipe, Tag
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from .models import Recipe, IngredientAmount, Ingredient
from django.contrib.auth.decorators import login_required
from .forms import RecipeForm
from .utils import get_ingredients

User = get_user_model()


def index(request):

    tags_selected = request.GET.getlist('filters', default=['breakfast', 'lunch', 'dinner'])
    recipe_list = Recipe.objects.filter(
        tags__slug__in=tags_selected
    ).select_related(
        'author'
    ).prefetch_related(
        'tags'
    ).distinct()

    tags_all = Tag.objects.all()

    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'index.html', {
        'page': page,
        'paginator': paginator,
        'tags': tags_all,
    })


@login_required
def subscription(request):
    user = request.user
    authors = User.objects.filter(
        following__follower=user).prefetch_related("recipe_author")

    paginator = Paginator(authors, 6)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)

    return render(request, 'subscription.html', {
        'page': page,
        'paginator': paginator
    })


@login_required
def favorites(request):
    user = request.user
    tags_selected = request.GET.getlist('filters', default=['breakfast', 'lunch', 'dinner'])

    recipes = Recipe.objects.filter(
        favorite_recipe__user=user
    ).all()

    paginator = Paginator(recipes, 6)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)

    tags_all = Tag.objects.all()

    return render(request, 'favorites.html', {
        'page': page,
        'paginator': paginator,
        'tags': tags_all
    })


def user_recipe_view_page(request, username):
    author = get_object_or_404(User, username=username)
    tags_selected = request.GET.getlist('filters', default=['breakfast', 'lunch', 'dinner'])
    recipes = Recipe.objects.filter(author_id=author.id)

    paginator = Paginator(recipes, 6)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)

    tags_all = Tag.objects.all()

    return render(request, 'user_recipe_view_page.html', {
        'page': page,
        'paginator': paginator,
        'author': author,
        'tags': tags_all,
    })


def recipe_view_page(request, username, recipe_id):

    author = get_object_or_404(User, username=username)
    recipe = get_object_or_404(Recipe, id=recipe_id, author_id=author.id)
    ingredients = IngredientAmount.objects.filter(recipe_id=recipe_id)

    return render(request, 'recipe_view_page.html', {
        'author': author,
        'recipe': recipe,
        'ingredients': ingredients,
    })


@login_required
def recipe_edit_page(request, username, recipe_id):

    recipe = get_object_or_404(Recipe, pk=recipe_id)

    if request.user != recipe.author or username != request.user.username:
        return redirect('recipe_view_page', username=recipe.author, recipe_id=recipe.pk)

    if request.method == 'POST':
        form = RecipeForm(request.POST or None, request.FILES or None, instance=recipe)

        if form.is_valid():
            form.save()
            recipe.ingredient_amount.all().delete()


            ingredients = get_ingredients(request)
            for title, amount in ingredients.items():
                ingredient = get_object_or_404(Ingredient, title=title)
                ingredient_amount = IngredientAmount(amount=amount, ingredient=ingredient, recipe=recipe)
                ingredient_amount.save()

            return redirect('recipe_view_page', username=recipe.author, recipe_id=recipe.pk)

    form = RecipeForm(instance=recipe)
    ingredients = IngredientAmount.objects.filter(recipe_id=recipe_id)

    return render(request, 'recipe_edit_page.html', {'form': form, 'recipe': recipe, 'ingredients': ingredients})


@login_required
def recipe_add_page(request):

    if request.method == 'POST':
        form = RecipeForm(request.POST or None, files=request.FILES or None)
        ingredients = get_ingredients(request)

        if not bool(ingredients):
            form.add_error(None, "Добавьте хотя бы один ингредиент")

        elif form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()

            ingredient_amounts = [IngredientAmount(
                amount=amount, ingredient=Ingredient.objects.get(title=title),
                recipe=recipe) for title, amount in ingredients.items()]

            IngredientAmount.objects.bulk_create(ingredient_amounts)
            form.save_m2m()
            return redirect('recipe_view_page', username=request.user, recipe_id=recipe.id)
    else:
        form = RecipeForm(files=request.FILES or None)
    return render(request, 'recipe_add_page.html', context={'form': form})
