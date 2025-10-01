from django.http import JsonResponse
from django.shortcuts import render
from .models import Ingredient
from django.shortcuts import get_object_or_404

def barcode_scanner(request):
    """
    Rende la pagina con lo scanner di codici a barre.
    """
    return render(request, 'kitchen/scanner.html')

def get_ingredient_by_barcode(request, barcode):
    """
    Recupera un ingrediente tramite il suo barcode e restituisce i dati in formato JSON.
    """
    try:
        ingredient = Ingredient.objects.get(barcode=barcode)
        data = {
            'id': ingredient.id,
            'name': ingredient.name,
            'unit': ingredient.get_unit_display(),
            'quantity_in_stock': ingredient.quantity_in_stock,
            'cost_per_unit': ingredient.cost_per_unit,
        }
        return JsonResponse(data)
    except Ingredient.DoesNotExist:
        return JsonResponse({'error': 'Ingrediente non trovato'}, status=404)
