from django.contrib import admin

from . import models


class IngredientInline(admin.TabularInline):
    def get_extra(self, request, obj=None, **kwargs):
        return 0 if obj else 1

    model = models.Ingredient.recipes.through


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [IngredientInline, ]

    fields = ('title', 'description', )

@admin.register(models.Ingredient)
class IngredientAdmin(admin.ModelAdmin):

    fields = ('name', 'description', )