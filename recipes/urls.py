from django.urls import path, include

from .views import RecipesList, RecipeDetail, RecipeCreate, RecipeUpdate, RecipeDelete, create_master_recipe

urlpatterns = [
    path("", RecipesList.as_view(), name="recipe-home"),
    path("<slugmaster>/<int:pk>/", RecipeDetail.as_view(), name="recipe-detail"),
    path("recipe/new/", create_master_recipe, name="recipe-create"),
    path("<slugmaster>/<int:pk>/update/", RecipeUpdate.as_view(), name="recipe-update"),
    path("<slugmaster>/<int:pk>/delete/", RecipeDelete.as_view(), name="recipe-delete"),
]
