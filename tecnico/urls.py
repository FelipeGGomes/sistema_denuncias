from django.urls import path
from . import views

app_name = 'tecnico'

urlpatterns = [
    path('dashboard/', views.tecnico_ver, name='tecnico_list'),
]