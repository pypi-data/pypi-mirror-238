from django.db import models


class Recipe(models.Model):
    def __str__(self):
        return self.title
    
    def descrivi(self):
        return self.description

    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()


class Ingredient(models.Model):

    def __str__(self):
        return self.title

    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    recipes = models.ManyToManyField(Recipe)
