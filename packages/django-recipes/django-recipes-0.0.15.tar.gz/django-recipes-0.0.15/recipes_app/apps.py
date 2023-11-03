import pathlib

from django.apps import AppConfig


class RecipesAppConfig(AppConfig):
    name = 'recipes_app'
    verbose_name = 'recipes'
    path = pathlib.Path(__file__).parent

    # def ready(self):
    #     from . import signals