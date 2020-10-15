from django import forms
from recipes.models import Material, Ingredient, QntIngredient


class NewRecipeForm(forms.Form):
    recipe_master__name = forms.CharField(
        label="Nom de la recette",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control ml-2"}),
    )
    recipe_nb_servings = forms.IntegerField(
        label="Portions",
        required=False,
        widget=forms.NumberInput(attrs={"class": "form-control ml-2"}),
    )
    recipe_prep_time = forms.IntegerField(
        label="Temps de préparation",
        required=False,
        widget=forms.NumberInput(attrs={"class": "form-control ml-2"}),
    )
    recipe_material = forms.ModelMultipleChoiceField(
        queryset=Material.objects.all().order_by("material"),
        label="Matériels",
        required=False,
    )
    recipe_instruction = forms.CharField(
        label="Instructions",
        max_length=1000,
        required=False,
        widget=forms.Textarea,
    )
    recipe_pic = forms.FileField(label="Photo", required=False)


class NewMaterialForm(forms.Form):
    material = forms.CharField(
        label="Ajouter materiel",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control ml-2"}),
    )


class NewIngredientForm(forms.Form):
    ingredientadd = forms.CharField(
        label="Ajouter ingredient",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control ml-2"}),
    )


class NewQntIngredientForm(forms.Form):
    qnt = forms.IntegerField(label="Qnt", required=False)
    ingredient = forms.ModelChoiceField(
        queryset=Ingredient.objects.all(), label="Ingredient", required=False
    )
