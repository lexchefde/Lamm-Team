from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile

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
