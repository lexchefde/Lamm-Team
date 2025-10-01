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


class Ingredient(models.Model):
    """
    Modello per un singolo ingrediente nell'inventario.
    """
    UNIT_CHOICES = (
        ('g', 'Grammi'),
        ('kg', 'Chilogrammi'),
        ('ml', 'Millilitri'),
        ('l', 'Litri'),
        ('pz', 'Pezzi'),
    )
    name = models.CharField(max_length=100, verbose_name="Nome Ingrediente", unique=True)
    barcode = models.CharField(max_length=100, unique=True, blank=True, null=True, verbose_name="Barcode")
    unit = models.CharField(max_length=5, choices=UNIT_CHOICES, verbose_name="Unità di Misura")
    quantity_in_stock = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Quantità in Magazzino")
    cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Costo per Unità (€)")

    def __str__(self):
        return f"{self.name} ({self.quantity_in_stock} {self.get_unit_display()})"

    class Meta:
        verbose_name = "Ingrediente"
        verbose_name_plural = "Ingredienti"
        ordering = ['name']


class Recipe(models.Model):
    """
    Modello per una ricetta, che include una lista di ingredienti.
    """
    name = models.CharField(max_length=200, verbose_name="Nome Ricetta")
    description = models.TextField(blank=True, verbose_name="Descrizione")
    instructions = models.TextField(verbose_name="Istruzioni")
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient', verbose_name="Ingredienti")

    def __str__(self):
        return self.name

    def calculate_food_cost(self):
        """
        Calcola il costo totale degli ingredienti per questa ricetta (food cost).
        """
        total_cost = 0
        for recipe_ingredient in self.recipeingredient_set.all():
            cost = recipe_ingredient.quantity * recipe_ingredient.ingredient.cost_per_unit
            total_cost += cost
        return total_cost

    @property
    def food_cost(self):
        """
        Proprietà per accedere al food cost calcolato.
        """
        return self.calculate_food_cost()

    class Meta:
        verbose_name = "Ricetta"
        verbose_name_plural = "Ricette"


class RecipeIngredient(models.Model):
    """
    Modello intermedio che collega una Ricetta a un Ingrediente, specificando la quantità.
    """
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name="Ricetta")
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, verbose_name="Ingrediente")
    quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Quantità Richiesta")

    def __str__(self):
        return f"{self.quantity} {self.ingredient.get_unit_display()} di {self.ingredient.name} per {self.recipe.name}"

    class Meta:
        verbose_name = "Ingrediente della Ricetta"
        verbose_name_plural = "Ingredienti della Ricetta"
        unique_together = ('recipe', 'ingredient')
