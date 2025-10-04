from django.urls import path
from . import views

app_name = 'tecnico'

urlpatterns = [
    path("dashboard/", views.denuncia_list, name="dashboard"),
    path("denuncia/<str:protocolo>/", views.denuncia_detail, name="denuncia_detail"),
    path('denuncia/aceitar/<str:protocolo>/', views.aceitar_denuncia, name='aceitar_denuncia'),
    path('minhas-denuncias/', views.dashboard, name='minhas_denuncias'),
    path('denuncia/detalhe/<str:protocolo>/', views.detalhe_tecnico, name='detalhe_denuncia'),
    
]