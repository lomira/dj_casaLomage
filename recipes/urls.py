from django.urls import path

from . import views

urlpatterns = [
    path("", views.RecipesList.as_view(), name="recipe-home"),
    path("<slug>/", views.RecipeDetail.as_view(), name="recipe-detail")
]
