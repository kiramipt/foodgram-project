from django.urls import path
from . import views

urlpatterns = [
    path("<username>/<recipe_id>/remove/", views.recipe_remove, name="recipe_remove")
]
