from django.contrib import admin

from .models import Ingredient, Tag, Recipe


class IngredientAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "unit",)
    list_filter = ("unit", "unit",)
    search_fields = ("title",)


class TagAdmin(admin.ModelAdmin):
    list_display = ("pk", 'title', 'slug', 'color')


class RecipeAdmin(admin.ModelAdmin):
    list_display = ("pk", "author", "title", "image", "description", "cooking_time", "pub_date")
    list_filter = ("tags", )
    search_fields = ("description",)


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
