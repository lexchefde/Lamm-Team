from decimal import Decimal
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile, TemperatureRecord, CleaningRecord, Ingredient, Recipe, RecipeIngredient

class ProfileModelTest(TestCase):
    """
    Test per verificare la creazione automatica del profilo utente.
    """
    def test_profile_creation_on_user_creation(self):
        """
        Verifica che un profilo venga creato quando un nuovo utente si registra.
        """
        # Crea un nuovo utente
        user = User.objects.create_user(username='testuser', password='password123')
        # Verifica che il profilo sia stato creato
        self.assertIsNotNone(user.profile)
        # Verifica che il profilo sia collegato all'utente corretto
        self.assertEqual(user.profile.user, user)


class HACCPModelsTest(TestCase):
    """
    Test per i modelli del modulo HACCP.
    """
    def setUp(self):
        """
        Prepara i dati necessari per i test, come un utente di esempio.
        """
        self.user = User.objects.create_user(username='haccp_tester', password='password123')

    def test_create_temperature_record(self):
        """
        Verifica la corretta creazione di una registrazione di temperatura.
        """
        record = TemperatureRecord.objects.create(
            equipment_name='Frigorifero 1',
            temperature=4.5,
            recorded_by=self.user
        )
        self.assertEqual(record.equipment_name, 'Frigorifero 1')
        self.assertEqual(record.recorded_by, self.user)
        self.assertEqual(TemperatureRecord.objects.count(), 1)

    def test_create_cleaning_record(self):
        """
        Verifica la corretta creazione di una registrazione di pulizia.
        """
        record = CleaningRecord.objects.create(
            area_or_equipment='Banco da lavoro',
            completed_by=self.user,
            notes='Pulizia standard.'
        )
        self.assertEqual(record.area_or_equipment, 'Banco da lavoro')
        self.assertEqual(record.completed_by, self.user)
        self.assertEqual(CleaningRecord.objects.count(), 1)


class KitchenManagementTest(TestCase):
    """
    Test per il modulo di gestione della cucina (inventario, ricette, food cost).
    """
    def setUp(self):
        """
        Prepara i dati per i test: ingredienti e una ricetta.
        """
        self.ingredient1 = Ingredient.objects.create(
            name="Pomodoro", unit='kg', quantity_in_stock=10, cost_per_unit=2.50
        )
        self.ingredient2 = Ingredient.objects.create(
            name="Pasta", unit='kg', quantity_in_stock=20, cost_per_unit=1.80
        )
        self.recipe = Recipe.objects.create(
            name="Pasta al Pomodoro",
            instructions="Cucinare la pasta e aggiungere il sugo."
        )

    def test_create_recipe_with_ingredients(self):
        """
        Verifica che una ricetta e i suoi ingredienti vengano creati correttamente.
        """
        RecipeIngredient.objects.create(
            recipe=self.recipe, ingredient=self.ingredient1, quantity=0.200
        )
        RecipeIngredient.objects.create(
            recipe=self.recipe, ingredient=self.ingredient2, quantity=0.100
        )
        self.assertEqual(self.recipe.ingredients.count(), 2)
        self.assertEqual(self.recipe.recipeingredient_set.count(), 2)

    def test_food_cost_calculation(self):
        """
        Verifica che il calcolo del food cost sia corretto.
        """
        # Aggiungo ingredienti alla ricetta
        RecipeIngredient.objects.create(
            recipe=self.recipe, ingredient=self.ingredient1, quantity=0.200  # 200g di pomodoro
        )
        RecipeIngredient.objects.create(
            recipe=self.recipe, ingredient=self.ingredient2, quantity=0.100  # 100g di pasta
        )

        # Calcolo manuale del costo atteso
        # Costo pomodoro: 0.200 kg * 2.50 €/kg = 0.50 €
        # Costo pasta: 0.100 kg * 1.80 €/kg = 0.18 €
        # Totale: 0.50 + 0.18 = 0.68 €
        expected_cost = Decimal('0.68')

        # Confronto con il costo calcolato dal modello
        self.assertAlmostEqual(self.recipe.food_cost, expected_cost, places=2)
