from django.contrib.auth import get_user_model
from django.db import models

from recipes.models import Recipe

User = get_user_model()


class Follow(models.Model):
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="follower")
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following")

    class Meta:
        unique_together = ("follower", "following")


class Favorite(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="favorite_user")
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="favorite_recipe")


class Purchases(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="purchase_user")
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="purchase_recipe")

    class Meta:
        unique_together = ("user", "recipe",)
