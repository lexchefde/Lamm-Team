from django.contrib import admin
from .models import Profile, TemperatureRecord, CleaningRecord

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
