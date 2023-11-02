from django.test import TestCase

from . import models


class RecipeTestCase(TestCase):
    def setUp(self):
        models.Recipe.objects.create(title="Pasta al pomodoro", description="Pasta al pomodoro, ricetta originale della nonna con salsa segreta")

    def test_field_name(self):
        """Recipe description is correctly extract"""
        pasta = models.Recipe.objects.get(title="Pasta al pomodoro")
        self.assertEqual(pasta.descrivi(), 'Pasta al pomodoro, ricetta originale della nonna con salsa segreta')
