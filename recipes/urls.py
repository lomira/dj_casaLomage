from django.urls import path

from .views import RecipesList, RecipeDetail, RecipeCreate, RecipeUpdate, RecipeDelete

urlpatterns = [
    path("", RecipesList.as_view(), name="recipe-home"),
    path("<slugmaster>/<int:pk>/", RecipeDetail.as_view(), name="recipe-detail"),
    path("recipe/new/", RecipeCreate.as_view(), name="recipe-create"),
    path("<slugmaster>/<int:pk>/update/", RecipeUpdate.as_view(), name="recipe-update"),
    path("<slugmaster>/<int:pk>/delete/", RecipeDelete.as_view(), name="recipe-delete"),
]
