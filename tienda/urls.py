from django.urls import path, include
from . import views
urlpatterns = [
    path('Registrar_Zapatilla/', views.Registrar_zapatilla, name='Registrar zapa')
]