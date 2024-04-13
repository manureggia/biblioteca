from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.db import models


# Create your models here.
class Libro(models.Model):
    titolo = models.CharField(max_length=200)
    autore = models.CharField(max_length=50)
    pagine = models.IntegerField(default=100)

    def __str__(self):
        out = self.titolo + " di " + self.autore + " ha " + str(self.copie.all().count()) + ' copie'
        return out

    class Meta:
        verbose_name_plural = 'Libri'

    def get_availables(self):
        return self.copie.filter(data_prestito__isnull=True).count()


class Copia(models.Model):
    data_prestito = models.DateTimeField(default=None, null=True)
    scaduto = models.BooleanField(default=False)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, related_name='copie')

    def __str__(self):
        out = "Copia di" + self.libro.titolo + " di " + self.libro.autore + ":"
        if self.scaduto:
            out += " Copia Scaduta"
        else:
            out += "Copia non scaduta"
        return out


class CustomUser(models.Model):
     #Altri campi utente personalizzati
    prestiti_ids = my_custom_field = models.CharField(max_length=100, blank=True, null=True)

