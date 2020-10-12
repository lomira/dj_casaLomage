from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Ingredient(models.Model):
    ingredient = models.CharField(max_length=25)

    def __str__(self):
        return self.ingredient


class Material(models.Model):
    material = models.CharField(max_length=25)

    def __str__(self):
        return self.material


class Recipe(models.Model):
    name = models.CharField(max_length=100)
    pic = models.ImageField(default="default.jpg", upload_to="recipe_pics")
    prep_time = models.IntegerField()
    material = models.ManyToManyField(Material, related_name="recipe")
    nb_servings = models.IntegerField()
    instruction = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    last_modifed_on = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class QntIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.quantiyty} x {self.material}"

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return self.author