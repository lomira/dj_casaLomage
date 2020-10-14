from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import QueryDict
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from recipes.models import RecipeMaster, Recipe, QntIngredient, Material, Ingredient
from .forms import (
    NewRecipeForm,
    NewMaterialForm,
    NewIngredientForm,
    NewQntIngredientForm,
)

# Index page
class RecipesList(ListView):
    model = Recipe
    context_object_name = "recipe_list"
    template_name = "recipes/all_recipes.html"
    paginate_by = 1

    def get_queryset(self):
        # Keeping the lastest recipes for each master recipe (with a recipe)
        allmaster = RecipeMaster.objects.all()
        subset = [Recipe.objects.filter(recipe_master=x) for x in allmaster]
        subset = filter(None, subset)
        lastest = [x.latest("last_modifed_on") for x in subset]
        return lastest

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


class RecipeUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Recipe
    fields = ["pic", "prep_time", "material", "nb_servings", "instruction"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        recipe = self.get_object()
        return self.request.user == recipe.recipe_master.author

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Mettre à jour une recette"
        return context


class RecipeDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Recipe
    success_url = "/"

    def test_func(self):
        recipe = self.get_object()
        return self.request.user == recipe.recipe_master.author

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Supprimer une recette"
        return context


# TODO : Implémenter ma propre view pour que crée d'un coup, un master, une recette et les ingrédients
class RecipeCreate(LoginRequiredMixin, CreateView):
    model = Recipe
    fields = ["pic", "prep_time", "material", "nb_servings", "instruction"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Créer une recette"
        return context


def create_master_recipe(request):
    # if this is a POST request we need to process the form data
    # TODO handle file upload

    if request.method == "POST":
        # create a form instances and populate it with data from the request:
        master_form = NewRecipeForm(request.POST)
        material_form = NewMaterialForm(request.POST)
        qntingredient_form = NewQntIngredientForm(request.POST)
        ingredient_form = NewIngredientForm(request.POST)
        # print(request.POST)

        # 1st case : adding material
        if material_form.is_valid() and "btn_material" in request.POST:
            obj = material_form.cleaned_data["material"]
            obj = Material.objects.create(material=obj)
            obj.save()
            material_form = NewMaterialForm()  # Empty form no redirect

        # 2nd case : adding ingredient
        if ingredient_form.is_valid() and "btn_ingredient" in request.POST:
            obj = ingredient_form.cleaned_data["ingredientadd"]
            obj = Ingredient.objects.create(ingredient=obj)
            obj.save()
            ingredient_form = NewIngredientForm()  # Empty form no redirect

        # 3rd case: addition combo ingredient elements
        if qntingredient_form.is_valid() and "btn_add_qnt_ingredient" in request.POST:
            qnt = qntingredient_form.cleaned_data["qnt"]
            ingredient = qntingredient_form.cleaned_data["ingredient"]
            # qntingredient is used to keep track of all ingredients
            if current := request.POST.getlist("listqntingr"):
                listqntingr = current + [f"{qnt} x {ingredient}"]
            else:
                listqntingr = [f"{qnt} x {ingredient}"]
            qntingredient_form = NewQntIngredientForm()

        # check whether it's valid:
        if qntingredient_form.is_valid() and "master" in request.POST:
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect("/")

    # if a GET (or any other method) we'll create a blank form
    else:
        master_form = NewRecipeForm()
        material_form = NewMaterialForm()
        qntingredient_form = NewQntIngredientForm()
        ingredient_form = NewIngredientForm()
        listqntingr = ""

    context = {
        "master_form": master_form,
        "material_form": material_form,
        "ingredient_form": ingredient_form,
        "qntingredient_form": qntingredient_form,
        "listqntingr": listqntingr,
    }

    return render(request, "recipes/create_recipe.html", context)
