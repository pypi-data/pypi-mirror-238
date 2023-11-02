from django.test import TestCase

from . import models


class VistaRicetteTest(TestCase):
    def setUp(self):
        self.ricetta = models.Recipe.objects.create(title="Pasta al pomodoro", 
                        description="Pasta al pomodoro, ricetta originale della nonna con salsa segreta")

    def test_vista_elenco_ricette(self):
        response = self.client.get('/recipes_app/recipe/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pasta al pomodoro")

    def test_dettaglio_ricetta(self):
        response = self.client.get(f'/recipes_app/recipe/{self.ricetta.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pasta al pomodoro")
        self.assertContains(response, "Pasta al pomodoro, ricetta originale della nonna con salsa segreta")
