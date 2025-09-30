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


class TemperatureRecord(models.Model):
    """
    Registrazione della temperatura per attrezzature come frigoriferi e congelatori.
    """
    equipment_name = models.CharField(max_length=100, verbose_name="Attrezzatura")
    temperature = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Temperatura (°C)")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Data e Ora")
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Registrato da")

    def __str__(self):
        return f"{self.equipment_name} - {self.temperature}°C il {self.timestamp.strftime('%d/%m/%Y %H:%M')}"

    class Meta:
        verbose_name = "Registrazione Temperatura"
        verbose_name_plural = "Registrazioni Temperature"
        ordering = ['-timestamp']


class CleaningRecord(models.Model):
    """
    Registrazione delle attività di pulizia e sanificazione.
    """
    area_or_equipment = models.CharField(max_length=100, verbose_name="Area/Attrezzatura Pulita")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Data e Ora")
    completed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Completato da")
    notes = models.TextField(blank=True, null=True, verbose_name="Note Aggiuntive")

    def __str__(self):
        return f"Pulizia di {self.area_or_equipment} il {self.timestamp.strftime('%d/%m/%Y %H:%M')}"

    class Meta:
        verbose_name = "Registrazione Pulizia"
        verbose_name_plural = "Registrazioni Pulizie"
        ordering = ['-timestamp']
