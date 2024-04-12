from django.contrib import messages
from django.shortcuts import render, redirect

from gestione.forms import ModificaLibroForm
from gestione.models import Libro


# Create your views here.

def lista_libri(request):
    template_name = "gestione/listalibri.html"

    ctx = { "title": "Lista Libri",
            "listalibri": Libro.objects.all()}
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