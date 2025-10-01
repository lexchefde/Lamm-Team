from decimal import Decimal
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile, TemperatureRecord, CleaningRecord, Ingredient, Recipe, RecipeIngredient, Notification

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


class NotificationSignalTest(TestCase):
    """
    Test per il segnale che genera notifiche quando le scorte sono basse.
    """
    def test_notification_creation_on_low_stock(self):
        """
        Verifica che una notifica venga creata quando la quantità di un ingrediente
        scende al di sotto della sua soglia minima.
        """
        # Crea un ingrediente con una soglia minima
        ingredient = Ingredient.objects.create(
            name="Farina",
            unit='kg',
            quantity_in_stock=10,
            cost_per_unit=1.00,
            minimum_threshold=5  # Soglia minima di 5 kg
        )

        # La quantità iniziale è sopra la soglia, nessuna notifica dovrebbe esistere
        self.assertEqual(Notification.objects.count(), 0)

        # Aggiorna la quantità portandola sotto la soglia
        ingredient.quantity_in_stock = 4
        ingredient.save()

        # Ora dovrebbe esistere una notifica
        self.assertEqual(Notification.objects.count(), 1)
        notification = Notification.objects.first()
        self.assertEqual(notification.ingredient, ingredient)
        self.assertIn("scorta di Farina è bassa", notification.message)

    def test_no_notification_if_stock_is_sufficient(self):
        """
        Verifica che non venga creata alcuna notifica se la quantità
        rimane al di sopra della soglia minima.
        """
        # Crea un ingrediente e aggiorna la quantità, ma sempre sopra la soglia
        ingredient = Ingredient.objects.create(
            name="Zucchero",
            unit='kg',
            quantity_in_stock=10,
            cost_per_unit=1.20,
            minimum_threshold=2
        )
        ingredient.quantity_in_stock = 8
        ingredient.save()

        # Nessuna notifica dovrebbe essere stata creata
        self.assertEqual(Notification.objects.count(), 0)

    def test_no_duplicate_notifications(self):
        """
        Verifica che non vengano create notifiche duplicate per lo stesso
        ingrediente se la scorta rimane bassa.
        """
        # Crea un ingrediente e portalo sotto soglia
        ingredient = Ingredient.objects.create(
            name="Sale",
            unit='kg',
            quantity_in_stock=2,
            cost_per_unit=0.50,
            minimum_threshold=3
        )

        # La prima notifica viene creata
        self.assertEqual(Notification.objects.count(), 1)

        # Aggiorna di nuovo l'ingrediente, ma la quantità è ancora sotto soglia
        ingredient.quantity_in_stock = 1
        ingredient.save()

        # Non dovrebbe essere stata creata una nuova notifica
        self.assertEqual(Notification.objects.count(), 1)

        # Se la notifica viene letta, una nuova può essere creata
        notification = Notification.objects.first()
        notification.is_read = True
        notification.save()

        ingredient.quantity_in_stock = 0.5
        ingredient.save()
        self.assertEqual(Notification.objects.count(), 2)
