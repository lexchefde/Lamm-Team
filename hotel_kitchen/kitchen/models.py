from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    """
    Modello per estendere le informazioni dell'utente, aggiungendo il ruolo.
    """
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('chef', 'Chef'),
        ('aiuto_cuoco', 'Aiuto Cuoco'),
        ('sala', 'Sala'),
        ('reception', 'Reception'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=True)

    def __str__(self):
        return f'{self.user.username} - {self.get_role_display()}'

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Crea o aggiorna il profilo utente ogni volta che un oggetto User viene salvato.
    """
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
