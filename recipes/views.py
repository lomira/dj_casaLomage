from django.shortcuts import render
from django.views.generic import ListView, DetailView
from recipes.models import Recipe, QntIngredient

# Index page
class RecipesList(ListView):
    queryset = Recipe.objects.all().order_by("-created_on")
    
    context_object_name = "recipe_list"
    template_name = 'recipes/all_recipes.html'

class RecipeDetail(DetailView):
    model = Recipe
    context_object_name = "recipe"
    query_pk_and_slug=True
    template_name = 'recipes/one_recipe.html'
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the ingredients and quantity
        context['ingredients'] = QntIngredient.objects.filter(recipe=self.get_object().pk)
        return context