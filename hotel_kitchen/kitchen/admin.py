from django.contrib import admin
from .models import Profile, TemperatureRecord, CleaningRecord, Ingredient, Recipe, RecipeIngredient

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Configurazione per il modello Profile nell'interfaccia di amministrazione.
    """
    list_display = ('user', 'role')
    list_filter = ('role',)
    search_fields = ('user__username',)

@admin.register(TemperatureRecord)
class TemperatureRecordAdmin(admin.ModelAdmin):
    """
    Configurazione per il modello TemperatureRecord nell'amministrazione.
    """
    list_display = ('equipment_name', 'temperature', 'timestamp', 'recorded_by')
    list_filter = ('equipment_name', 'timestamp', 'recorded_by')
    search_fields = ('equipment_name', 'recorded_by__username')
    date_hierarchy = 'timestamp'

@admin.register(CleaningRecord)
class CleaningRecordAdmin(admin.ModelAdmin):
    """
    Configurazione per il modello CleaningRecord nell'amministrazione.
    """
    list_display = ('area_or_equipment', 'timestamp', 'completed_by')
    list_filter = ('area_or_equipment', 'timestamp', 'completed_by')
    search_fields = ('area_or_equipment', 'completed_by__username')
    date_hierarchy = 'timestamp'

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """
    Configurazione per il modello Ingredient nell'amministrazione.
    """
    list_display = ('name', 'quantity_in_stock', 'unit', 'cost_per_unit')
    list_filter = ('unit',)
    search_fields = ('name',)

class RecipeIngredientInline(admin.TabularInline):
    """
    Permette di modificare gli ingredienti direttamente nella pagina della ricetta.
    """
    model = RecipeIngredient
    extra = 1  # Numero di righe extra da mostrare

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """
    Configurazione per il modello Recipe nell'amministrazione.
    """
    inlines = [RecipeIngredientInline]
    list_display = ('name', 'display_food_cost')
    readonly_fields = ('food_cost',)
    search_fields = ('name', 'ingredients__name')

    def display_food_cost(self, obj):
        """
        Formatta il food cost per la visualizzazione nell'elenco.
        """
        return f"€ {obj.food_cost:.2f}"
    display_food_cost.short_description = "Food Cost"
