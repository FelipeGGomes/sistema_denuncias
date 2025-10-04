from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .forms import DenunciaForm, DenunciaSearchForm, AdminDenunciaUpdateForm
from .models import Denuncia, Categoria, LogDenuncia
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
import json
from io import BytesIO 
from xhtml2pdf import pisa 
from datetime import datetime
from django.template.loader import render_to_string 

from django.shortcuts import render, redirect
from .forms import DenunciaForm

def denuncia_create_view(request):
    if request.method == "POST":
        form = DenunciaForm(request.POST, request.FILES)  # Recebe tanto os dados quanto o arquivo
        if form.is_valid():
            denuncia = form.save()
            print(f"Denúncia salva com sucesso: {denuncia.protocolo}")# Salva os dados no banco
            protocolo = denuncia.protocolo  # Pega o protocolo da denúncia
            return redirect('denuncias:denuncia-success', protocolo=protocolo)  # Redireciona para a página de sucesso
        else:
            print(f"Erro ao salvar denúncia: {form.errors}")
            # Caso o formulário não seja válido, renderiza o formulário novamente com erros
            return render(request, 'denuncias/form.html', {'form': form})
    else:
        form = DenunciaForm()  # Se não for um POST, renderiza o formulário vazio

    return render(request, 'denuncias/form.html', {'form': form})
def denuncia_success_view(request, protocolo):
    denuncia = get_object_or_404(Denuncia, protocolo=protocolo)
    return render(request, "denuncias/success.html", {"denuncia": denuncia})
def denuncia_search_view(request):
    form = DenunciaSearchForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        protocolo = form.cleaned_data['protocolo']
        if Denuncia.objects.filter(protocolo=protocolo).exists():
            # CORREÇÃO AQUI: Passa o argumento nomeado 'protocolo'
            return redirect('denuncias:denuncia-detail', protocolo=protocolo) 
        else:
            form.add_error('protocolo', 'Protocolo não encontrado.')

    return render(request, 'denuncias/search.html', {'form': form})
def denuncia_detail_view(request, protocolo):
    denuncia = get_object_or_404(Denuncia, protocolo=protocolo)
    logs = LogDenuncia.objects.filter(denuncia=denuncia)
    
    return render(request, 'denuncias/detail.html', {'denuncia': denuncia, 'logs': logs})

# --- Views Administrativas ---
@staff_member_required
def admin_denuncia_list_view(request):
    denuncias = Denuncia.objects.select_related('categoria', 'subcategoria').order_by('-data_criacao')
    
    # Filtros
    status_filter = request.GET.get('status')
    categoria_filter = request.GET.get('categoria')
    
    if status_filter:
        denuncias = denuncias.filter(status=status_filter)
    if categoria_filter:
        denuncias = denuncias.filter(categoria_id=categoria_filter)
    
    categorias = Categoria.objects.all()
    
    context = {
        'denuncias': denuncias,
        'categorias': categorias,
        'status_choices': Denuncia.STATUS_CHOICES,
    }
    return render(request, 'denuncias/admin_denuncia_list.html', context)

@staff_member_required
def admin_denuncia_update_view(request, protocolo):
    denuncia = get_object_or_404(Denuncia, protocolo=protocolo)
    form = AdminDenunciaUpdateForm(request.POST or None, instance=denuncia)
    
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('admin-denuncia-list')
    
    return render(request, 'denuncias/admin_denuncia_update.html', {'form': form, 'denuncia': denuncia})

@staff_member_required
def admin_denuncia_dashboard_view(request):
    # Estatísticas para o dashboard
    total_denuncias = Denuncia.objects.count()
    denuncias_pendentes = Denuncia.objects.filter(status='PENDENTE').count()
    denuncias_analise = Denuncia.objects.filter(status='EM_ANALISE').count()
    denuncias_resolvidas = Denuncia.objects.filter(status='RESOLVIDO').count()
    
    # Denúncias por categoria
    denuncias_por_categoria = []
    for categoria in Categoria.objects.all():
        count = Denuncia.objects.filter(categoria=categoria).count()
        if count > 0:
            denuncias_por_categoria.append({
                'categoria': categoria.nome,
                'count': count
            })
    
    # Últimas denúncias
    ultimas_denuncias = Denuncia.objects.select_related('categoria', 'subcategoria').order_by('-data_criacao')[:10]
    
    context = {
        'total_denuncias': total_denuncias,
        'denuncias_pendentes': denuncias_pendentes,
        'denuncias_analise': denuncias_analise,
        'denuncias_resolvidas': denuncias_resolvidas,
        'denuncias_por_categoria': denuncias_por_categoria,
        'ultimas_denuncias': ultimas_denuncias,
    }
    
    return render(request, 'denuncias/admin_dashboard.html', context)

def home_view(request):
    return render(request, 'denuncias/index.html')




def denuncias_form_view(request): # Renomeado para maior clareza
    # Filtra apenas as categorias ativas e ordena
    categorias = Categoria.objects.filter(ativo=True).order_by('ordem')
    
    # Se você estiver usando um ModelForm ou Form Django, passe a instância:
    form = DenunciaForm() 
    
    # Se você quiser passar as categorias separadamente para um formulário HTML customizado:
    context = {
        'form': form,
        'categorias': categorias # Passando as categorias
    }
    
    return render(request, 'denuncias/form.html', context)


# Função auxiliar para conversão
def render_to_pdf(template_src, context_dict={}):
    

    html = render_to_string(template_src, context_dict)
    
    result = BytesIO()
    
    # 3. Converte o HTML para PDF (target=result armazena no buffer)
    # A função pisa.pisaDocument lida com a conversão
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    
    # 4. Retorna o conteúdo do PDF ou False em caso de erro
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    
    return HttpResponse('Houve um erro ao gerar o PDF: %s' % pdf.err, status=500)


def denuncia_pdf_view(request, protocolo):
    denuncia = get_object_or_404(Denuncia, protocolo=protocolo)

    # Obter dados da denúncia para o template (como no exemplo anterior)
    context = {
        'denuncia': denuncia,
        'protocolo': denuncia.protocolo,
        'titulo_protocolo': getattr(denuncia, 'titulo', f"Denúncia: {denuncia.protocolo}"), 
        'categoria_nome': denuncia.categoria.nome if denuncia.categoria else 'N/A',
        'data_registro': denuncia.data_criacao.strftime("%d/%m/%Y - %H:%M"),
        'status_display': denuncia.get_status_display(),
        'localizacao': denuncia.endereco, 
        'data_emissao': datetime.now().strftime("%d/%m/%Y às %H:%M"),
        'request': request # Necessário para URLs absolutas (QR Code, etc.)
    }

    # Gera e retorna o PDF
    response = render_to_pdf('pdf/print.html', context)
    
    # Configura o nome do arquivo para download
    response['Content-Disposition'] = f'attachment; filename="Protocolo_{denuncia.protocolo}.pdf"'

    return response



def ver_pdf(request):
    return render(request, 'pdf/print.html')
