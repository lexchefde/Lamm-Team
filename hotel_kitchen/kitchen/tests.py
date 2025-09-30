from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile, TemperatureRecord, CleaningRecord

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
