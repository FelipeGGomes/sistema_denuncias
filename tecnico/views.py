from django.shortcuts import render
from .models import Tecnico
from denuncia.models import Denuncia, Logdenuncia

def denuncia_list(request):
    denuncias = Denuncia.objects.filter(status='NÃO_ATRIBUIDO')
    return render(request, 'dashboard.html', {'denuncias': denuncias})


def tecnico_ver(request):
    return render(request, 'dashboard.html')



