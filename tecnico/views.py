from django.utils import timezone
from pyexpat.errors import messages
from venv import logger
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from tecnico.forms import UpdateStatusForm
from .models import Tecnico
from denuncias.models import Denuncia, LogDenuncia
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

@login_required
def denuncia_list(request):
    denuncias = Denuncia.objects.filter(status='NÃO_ATRIBUIDO')
    denuncias_em_analise = Denuncia.objects.filter(status='EM_ANALISE')
    denuncias_em_andamento = Denuncia.objects.filter(status='EM_ANDAMENTO')
    denuncias_resolvidas = Denuncia.objects.filter(status='RESOLVIDA')
    denuncias_arquivadas = Denuncia.objects.filter(status='ARQUIVADA')
    
    return render(request, 'dashboard.html', {
        'denuncias': denuncias,
        'denuncias_em_analise': denuncias_em_analise,
        'denuncias_em_andamento': denuncias_em_andamento,
        'denuncias_resolvidas': denuncias_resolvidas,
        'denuncias_arquivadas': denuncias_arquivadas,
    })

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
    
    return render(request, 'teste.html', {'denuncia_user': denuncia_user})



@login_required
def dashboard(request):
    denuncias_nao_atribuidas = Denuncia.objects.filter(
        tecnico__isnull=True,
        status='NÃO_ATRIBUIDO'
    )

    minhas_denuncias_lista = Denuncia.objects.filter(
        tecnico=request.user
    ).exclude(
        status__in=['RESOLVIDA', 'ARQUIVADA']
    )

    sort_field = request.GET.get('sort', 'data_atualizacao') 
    order = request.GET.get('order', 'desc')
    

    valid_sort_fields = ['protocolo', 'titulo', 'categoria__nome', 'status', 'prioridade', 'data_atualizacao']
    if sort_field not in valid_sort_fields:
        sort_field = 'data_atualizacao' 

    order_prefix = '-' if order == 'desc' else ''
    minhas_denuncias_lista = minhas_denuncias_lista.order_by(f'{order_prefix}{sort_field}')

   
    paginator = Paginator(minhas_denuncias_lista, 15)
    page_number = request.GET.get('page', 1)

    try:

        minhas_denuncias_paginadas = paginator.page(page_number)
    except PageNotAnInteger:
        minhas_denuncias_paginadas = paginator.page(1)
    except EmptyPage:
        minhas_denuncias_paginadas = paginator.page(paginator.num_pages)

    context = {
        'denuncias_nao_atribuidas': denuncias_nao_atribuidas,
        'minhas_denuncias': minhas_denuncias_paginadas,
        'current_sort': sort_field,
        'current_order': order,
    }


    return render(request, 'denuncia_tecnico.html', context)

@login_required
def detalhe_tecnico(request, protocolo):
    denuncia = get_object_or_404(Denuncia, protocolo=protocolo)
    if not request.user.is_superuser and denuncia.tecnico != request.user:
        messages.error(request, "Você não tem permissão para ver esta denúncia.")
        return redirect('tecnico:dashboard')

    if request.method == 'POST':
        form = UpdateStatusForm(request.POST)
        if form.is_valid():
            novo_status = form.cleaned_data['status']
            comentario = form.cleaned_data['comentario']

            denuncia.status = novo_status
            
            if novo_status == 'RESOLVIDA':
                denuncia.data_resolucao = timezone.now()
            
            denuncia.save()

            LogDenuncia.objects.create(
                denuncia=denuncia,
                usuario=request.user,
                tipo_acao='STATUS',
                acao=f'Status alterado para "{denuncia.get_status_display()}"',
                descricao=comentario
            )

            messages.success(request, f'O status da denúncia {denuncia.protocolo} foi atualizado com sucesso.')
            return redirect('tecnico:denuncia_detail', protocolo=denuncia.protocolo)
    
    else:
        
        form = UpdateStatusForm()

    logs = LogDenuncia.objects.filter(denuncia=denuncia).order_by('-data_acao')

    context = {
        'denuncia': denuncia,
        'form': form,
        'logs': logs,
    }
    return render(request, 'detalhe_tecnico.html', context)
