from django.shortcuts import render, redirect, get_object_or_404
from .models import Recipe, Tag
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from .models import Recipe, IngredientAmount

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

    for recipe in page:
        print("lunch" in recipe.tags.all())
        print(recipe.tags.all()[0].slug)
        print()

    return render(request, 'index.html', {
        'page': page,
        'paginator': paginator,
        'tags': tags_all,
    })


def user_page(request, username):
    author = get_object_or_404(User, username=username)
    # tags, tags_filter = tag_collect(request)
    # if tags_filter:
    #     recipes = Recipe.objects.filter(tags_filter).filter(
    #         author_id=author.id).all()
    # else:
    tags_selected = request.GET.getlist('filters', default=['breakfast', 'lunch', 'dinner'])

    recipes = Recipe.objects.filter(author_id=author.id)

    paginator = Paginator(recipes, 6)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)

    return render(request, 'user_page.html', {
        'page': page,
        'paginator': paginator,
        'tags': tags_selected,
        'author': author
    })


def recipe_page(request, username, recipe_id):

    author = get_object_or_404(User, username=username)
    recipe = get_object_or_404(Recipe, id=recipe_id, author_id=author.id)
    ingredients = IngredientAmount.objects.filter(recipe_id=recipe_id)

    return render(request, 'recipe_page.html', {
        'recipe': recipe,
        'ingredients': ingredients,
        'author': author
    })
