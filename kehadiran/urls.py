from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('input/', views.input_absen, name='input_absen'),
    path('rekap/', views.rekap_bulanan, name='rekap_bulanan'),
]