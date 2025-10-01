from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'denuncias'

urlpatterns = [
    # Views públicas
    path('', views.home_view, name='home'),
    path('nova/', views.denuncia_create_view, name='denuncia-create'),
    path('sucesso/<str:protocolo>/', views.denuncia_success_view, name='denuncia-success'),
    path('consultar/', views.denuncia_search_view, name='denuncia-search'),
    path('detalhe/<str:protocolo>/', views.denuncia_detail_view, name='denuncia-detail'),
    
    # API para subcategorias dinâmicas

    # Views administrativas
    path('admin/denuncias/', views.admin_denuncia_list_view, name='admin-denuncia-list'),
    path('admin/denuncias/<str:protocolo>/editar/', views.admin_denuncia_update_view, name='admin-denuncia-update'),
    path('admin/dashboard/', views.admin_denuncia_dashboard_view, name='admin-dashboard'),
    path('pdf/<str:protocolo>/', views.denuncia_pdf_view, name='pdf-view'),
    path('modelo/', views.ver_pdf, name='modelo-pdf'),

    
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)