from django.urls import path
from . import views

app_name = 'tecnico'

urlpatterns = [
    path("dashboard/", views.denuncia_list, name="dashboard"),
    path("denuncia/<str:protocolo>/", views.denuncia_detail, name="denuncia_detail"),
    path('denuncia/aceitar/<str:protocolo>/', views.aceitar_denuncia, name='aceitar_denuncia'),
    path('minhas-denuncias/', views.dashboard, name='minhas_denuncias'),
    path('denuncia/detalhe/<str:protocolo>/', views.detalhe_tecnico, name='detalhe_denuncia'),
    path('perfil/', views.perfil_tecnico, name='perfil'),
    path('alterar-email/', views.alterar_email, name='alterar_email'),
    path('alterar-senha/', views.alterar_senha, name='alterar_senha'),
    
]