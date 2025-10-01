from django.urls import path
from . import views

app_name = 'kitchen'

urlpatterns = [
    path('scanner/', views.barcode_scanner, name='barcode_scanner'),
    path('api/ingredient/barcode/<str:barcode>/', views.get_ingredient_by_barcode, name='get_ingredient_by_barcode'),
]