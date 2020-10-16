from django.shortcuts import render
from .models import Recipe, Tag
from django.core.paginator import Paginator


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
        'all_tags': tags_all,
        'tags_list': tags_selected,
    })

