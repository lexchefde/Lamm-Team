from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Configurazione per il modello Profile nell'interfaccia di amministrazione.
    """
    list_display = ('user', 'role')
    list_filter = ('role',)
    search_fields = ('user__username',)
