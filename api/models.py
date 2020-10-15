from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Ingredient(models.Model):
    title = models.CharField(max_length=255)
    unit = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class IngredientAmount(models.Model):
    amount = models.IntegerField()
    ingredient = models.ForeignKey('Ingredient', on_delete=models.CASCADE)
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)


class Tag(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    color = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipe_author'
    )
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='image/')
    description = models.TextField()
    ingredient = models.ManyToManyField(
        Ingredient, through=IngredientAmount
    )
    tags = models.ManyToManyField(Tag, related_name='recipes')
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    cooking_time = models.IntegerField(default=10)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-pub_date', )
