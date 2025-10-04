from pyexpat.errors import messages
from venv import logger
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Tecnico
from denuncias.models import Denuncia, LogDenuncia
from django.views.decorators.http import require_POST

@login_required
def denuncia_list(request):
    denuncias = Denuncia.objects.filter(status='NÃO_ATRIBUIDO')
    return render(request, 'dashboard.html', {'denuncias': denuncias})

@login_required
def denuncia_detail(request, protocolo):
    denuncia = get_object_or_404(Denuncia, protocolo=protocolo)
    logs = denuncia.logs.all().order_by('-data_acao')

    return render(request, 'denuncia_detail.html', {
        "denuncia": denuncia,
        "logs": logs,
    })
    


@login_required
@require_POST
def aceitar_denuncia(request, protocolo):
    try:
        denuncia = get_object_or_404(Denuncia, protocolo=protocolo)

        if denuncia.tecnico:
            return JsonResponse({'success': False, 'message': 'Denúncia já atribuída.'}, status=409)

        # Dados anteriores para auditoria
        dados_anteriores = {
            'status': denuncia.status,
            'tecnico': denuncia.tecnico.username if denuncia.tecnico else None,
            'descricao': denuncia.descricao
        }

        # Atribui o técnico e altera o status
        denuncia.tecnico = request.user
        denuncia.status = 'EM_ANALISE'
        denuncia.save()

        # Dados novos para auditoria
        dados_novos = {
            'status': denuncia.status,
            'tecnico': request.user.username,
            'descricao': denuncia.descricao
        }

        LogDenuncia.objects.create(
            denuncia=denuncia,
            tipo_acao='EM_ANALISE',
            acao='Denúncia atribuída ao técnico',
            usuario=request.user,
            descricao=f'O técnico {request.user.username} assumiu a responsabilidade pela denúncia {denuncia.protocolo}.',
            dados_anteriores=dados_anteriores,
            dados_novos=dados_novos
        )

        return JsonResponse({'success': True, 'message': 'Denúncia aceita com sucesso!'})

    except Exception as e:
        logger.error(f"Erro ao aceitar denúncia: {e}", exc_info=True)
        return JsonResponse({'success': False, 'message': 'Erro no servidor.'}, status=500)



@login_required
def minhas_denuncias(request):
    denuncia_user = Denuncia.objects.filter(
        tecnico=request.user
    ).order_by('-data_criacao')
    
    return render(request, 'dashboard.html', {'denuncia_user': denuncia_user})