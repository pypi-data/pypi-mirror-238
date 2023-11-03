from rest_framework import routers

from . import views

urlpatterns = []

router = routers.SimpleRouter()

router.register(r'recipe', views.Recipe_View)
router.register(r'ingredient', views.Ingredient_View)

urlpatterns += router.urls