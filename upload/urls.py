from django.urls import path
from .views import *
urlpatterns = [
    path('excel/', export_import_excel ),
    path('create/', createStudent),
]
