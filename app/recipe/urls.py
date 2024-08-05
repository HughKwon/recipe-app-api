"""
URL mappings for the recipe app.
"""
from django.urls import (
    path,
    include,
)

# The DefaultRouter can be uses to create routes for all
# the different options available for that view
from rest_framework.routers import DefaultRouter

from recipe import views


router = DefaultRouter()
# create new endpoint API, assign all of the different endpoints from
# our recipe view set to that endoint
router.register('recipes', views.RecipeViewSet)
router.register('tags', views.TagViewSet)
router.register('ingredients', views.IngredientViewSet)

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls)),
]

