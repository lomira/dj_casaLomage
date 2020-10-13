from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from recipes.models import RecipeMaster, Recipe, QntIngredient


# Index page
class RecipesList(ListView):
    model = Recipe
    context_object_name = "recipe_list"
    template_name = "recipes/all_recipes.html"
    paginate_by = 1

    def get_queryset(self):
        allmaster = RecipeMaster.objects.all()
        return [
            Recipe.objects.filter(recipe_master=x).latest("last_modifed_on")
            for x in allmaster
        ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Toutes les recettes"
        return context


class RecipeDetail(DetailView):
    model = Recipe
    context_object_name = "recipe"
    template_name = "recipes/one_recipe.html"

    def get_queryset(self):
        return Recipe.objects.filter(
            pk=self.kwargs["pk"], recipe_master__slug=self.kwargs["slugmaster"]
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ingredients"] = QntIngredient.objects.filter(
            recipe=self.get_object().pk
        )
        context["page_title"] = self.get_object().recipe_master.name
        context["other_versions"] = Recipe.objects.filter(
            recipe_master__slug=self.kwargs["slugmaster"]
        ).order_by("last_modifed_on")
        return context


class RecipeCreate(LoginRequiredMixin, CreateView):
    model = Recipe
    fields = ["name", "pic", "prep_time", "material", "nb_servings", "instruction"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Créer une recette"
        return context


class RecipeUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Recipe
    fields = ["name", "pic", "prep_time", "material", "nb_servings", "instruction"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        recipe = self.get_object()
        if self.request.user == recipe.author:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Mettre à jour une recette"
        return context


class RecipeDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Recipe
    success_url = "/"

    def test_func(self):
        recipe = self.get_object()
        if self.request.user == recipe.author:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Supprimer une recette"
        return context