from django.contrib import admin

from recipes.models import (
    Ingredient,
    Material,
    Recipe,
    Comment,
    QntIngredient,
    RecipeMaster,
)

# Register your models here.

admin.site.register(Ingredient)
admin.site.register(Material)
admin.site.register(Recipe)
admin.site.register(Comment)
admin.site.register(QntIngredient)
admin.site.register(RecipeMaster)
