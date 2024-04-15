from datetime import datetime

from django.contrib import messages
from django.shortcuts import render, redirect

from gestione.forms import ModificaLibroForm
from gestione.models import Libro, Copia


# Create your views here.

def lista_libri(request):
    template_name = "gestione/listalibri.html"

    ctx = { "title": "Lista Libri",
            "listalibri": Libro.objects.all(),
            "request": request
            }
    return render(request, template_name, ctx)

def mattoni(request):
    template_name = "gestione/listalibri.html"
    lista_filtrata = Libro.objects.filter(pagine__gt= 300)
    ctx = {"title": "Lista Libri",
           "listalibri": lista_filtrata}
    return render(request, template_name, ctx)

def dettaglio_libro(request, id):
    libro = Libro.objects.get(pk=id)
    template_name = "gestione/dettaglio-libro.html"
    ctx = {"libro": libro}
    return render(request, template_name, ctx)


def edita_libro(request, id):
    libro = Libro.objects.get(id=id)
    if request.method == "POST":
        form = ModificaLibroForm(request.POST, instance=libro)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Libro aggiornato con successo")
                return redirect('dettaglio', libro.pk)
            except:
                return redirect('lista')
    form = ModificaLibroForm(instance=libro)
    return render(request,'gestione/edita-libro.html',{'form': form})

def crea_libro(request):
    if request.method == "POST":
        form = ModificaLibroForm(request.POST)
        if form.is_valid():
            try:
                libro = form.save()
                return redirect('dettaglio', libro.id)
            except Exception as ex:
                messages.error(request, ex)
        messages.error(request, "Errore nella creazione, form non valido")
    form = ModificaLibroForm()
    return render(request,'gestione/crea-libro.html',{'form':form})

def presta_libro(request, id):
    libro = Libro.objects.get(pk=id)
    user = request.user
    if user.is_authenticated:
        copia = libro.copie.filter(data_prestito__isnull=True)[0] if libro.copie.filter(data_prestito__isnull=True).count() > 0 else None
        if copia:
            copia.utente_id = request.user.id
            copia.data_prestito = datetime.now()
            copia.save()
            messages.success(request, "Libro Prestato con successo")
            return redirect('lista')
        messages.error(request,"Non sono presenti copie di questo libro")
        return redirect('lista')

def restituisci_libro(request, id):
    if request.user.is_authenticated:
        copie = Copia.objects.filter(utente_id=request.user.id, libro_id=id)
        if request.method == 'POST':
            if request.POST.get('id'):
                copia = Copia.objects.get(pk=request.POST.get('id'))
                copia.data_prestito = None
                copia.utente_id = None
                copia.scaduto = False
                copia.save()
                messages.success(request, "Libro restituito con successo")
                if copie.count() == 0:
                    return redirect('lista')
        if copie.count() > 0:
            template_name = 'gestione/restituisci-libro.html'
            return render(request, template_name, {'copie': copie})
        messages.warning(request, "Non sono presenti copie di questo libro in prestito a questo utente")
        return redirect('lista')
    messages.error(request,"Non Autenticato!")
    return redirect('lista')