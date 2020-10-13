from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from autoslug import AutoSlugField


class Ingredient(models.Model):
    ingredient = models.CharField(max_length=25)

    def __str__(self):
        return self.ingredient


class Material(models.Model):
    material = models.CharField(max_length=25)

    def __str__(self):
        return self.material


class RecipeMaster(models.Model):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(unique=True, populate_from="name", always_update=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("recipe-detail", kwargs={"slug": self.slug})


class Recipe(models.Model):
    recipe_master = models.ForeignKey(RecipeMaster, on_delete=models.CASCADE)

    created_on = models.DateTimeField(default=timezone.now)
    last_modifed_on = models.DateTimeField(auto_now=True)

    nb_servings = models.IntegerField()
    prep_time = models.IntegerField()
    material = models.ManyToManyField(Material, related_name="material_needed_in", blank=True)
    instruction = models.TextField()
    pic = models.ImageField(default="recipe_pics/default.jpg", upload_to="recipe_pics")

    def __str__(self):
        return f"{self.recipe_master.name} version {self.last_modifed_on}"



class QntIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.recipe.recipe_master} version {self.recipe.last_modifed_on} : {self.quantity} x {self.ingredient}"


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return self.author