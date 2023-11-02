from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny

from . import models, serializers

class Recipe_View(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication]
    permission_classes = [AllowAny]
    queryset = models.Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer

class Ingredient_View(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication]
    permission_classes = [AllowAny]
    queryset = models.Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer