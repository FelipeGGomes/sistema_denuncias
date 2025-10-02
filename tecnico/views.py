from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from .models import Tecnico
from denuncias.models import Denuncia, LogDenuncia

def denuncia_list(request):
    denuncias = Denuncia.objects.filter(status='NÃO_ATRIBUIDO')
    return render(request, 'dashboard.html', {'denuncias': denuncias})


def denuncia_detail(request, protocolo):
    denuncia = get_object_or_404(Denuncia, protocolo=protocolo)
    logs = denuncia.logs.all().order_by('-data_acao')

    return render(request, 'denuncia_detail.html', {
        "denuncia": denuncia,
        "logs": logs,
    })

def tecnico_ver(request):
    return render(request, 'dashboard.html')




