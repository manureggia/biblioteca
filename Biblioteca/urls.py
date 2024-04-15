from django.contrib import admin
from django.urls import path, include

from utils.database import erase_db, init_db, start_controllo_scadenza

urlpatterns = [
    path('admin/', admin.site.urls),
    path('gestione/', include('gestione.urls'))

]
#erase_db()
#init_db()
start_controllo_scadenza(5)