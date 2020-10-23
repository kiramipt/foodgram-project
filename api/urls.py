from django.urls import path
from . import views

urlpatterns = [
    path('api/subscriptions/', views.add_subscription, name='add_subscription'),
    path('api/subscriptions/<int:author_id>/', views.remove_subscription, name='remove_subscription'),

    path("api/favorites/", views.add_favorites, name='add_favorites'),
    path("api/favorites/<int:recipe_id>/", views.remove_favorites, name='remove_favorites'),

    path("<username>/<recipe_id>/remove/", views.recipe_remove, name="recipe_remove"),

]
