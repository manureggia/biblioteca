
from django.contrib import admin
from django.urls import path, include

from gestione.views import lista_libri, mattoni, dettaglio_libro, edita_libro, crea_libro, presta_libro

urlpatterns = [
    path('', lista_libri, name="lista"),
    path('lista/', lista_libri, name="lista"),
    path('mattoni/', mattoni, name="mattoni"),
    path('detail/<int:id>', dettaglio_libro, name="dettaglio"),
    path('edit/<int:id>', edita_libro, name="edita"),
    path('aggiungi/', crea_libro, name="crea_libro"),
    path('prestito/<int:id>', presta_libro, name="prestito")

]
