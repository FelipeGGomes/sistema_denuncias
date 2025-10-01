from django.contrib import admin
from .models import Categoria, Denuncia, LogDenuncia


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    # ADICIONADO: 'ativo' para visualização
    list_display = ['nome', 'ativo', 'get_denuncias_count'] 
    
    # ADICIONADO: 'ativo' para filtro lateral
    list_filter = ['ativo'] 
    
    search_fields = ['nome']
    
    def get_denuncias_count(self, obj):
        # Acesso ao Related Manager: o nome deve ser o related_name definido no ForeignKey de Denuncia.
        # Por padrão, se não for definido, é nome_do_modelo_set. (Ex: denuncia_set)
        # Assumindo que o related_name seja 'denuncias' como usado na sua função original.
        return obj.denuncias.count()
    get_denuncias_count.short_description = 'Denúncias'


@admin.register(Denuncia)
class DenunciaAdmin(admin.ModelAdmin):
    list_display = ['protocolo', 'categoria', 'status', 'prioridade', 'data_criacao', 'data_atualizacao']
    list_filter = ['status', 'prioridade', 'categoria']
    search_fields = ['protocolo', 'descricao', 'endereco']
    readonly_fields = ['protocolo', 'data_criacao']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('protocolo', 'categoria', 'status', 'prioridade')
        }),
        ('Detalhes da Denúncia', {
            'fields': ('descricao', 'endereco', 'foto', 'contato')
        }),
        # CORREÇÃO AQUI: 'observacoes' DEVE SER 'observacoes_internas'
        ('Observações Administrativas', { 
            'fields': ('observacoes_internas',), # O nome do campo foi corrigido
            'classes': ('collapse',),
        }),
        ('Datas', {
            'fields': ('data_criacao',),
            'classes': ('collapse',)
        }),
    )

    # Função opcional para otimizar consultas (seleciona categoria para evitar N+1 queries)
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('categoria')

# NOTA: O campo 'observacoes' foi adicionado no fieldsets, assumindo que ele exista no seu modelo Denuncia.



@admin.register(LogDenuncia)
class LogDenunciaAdmin(admin.ModelAdmin):
    list_display = ['denuncia', 'acao', 'data_acao', 'usuario']
    list_filter = ['acao', 'data_acao']
    search_fields = ['denuncia__protocolo', 'usuario__username']
    readonly_fields = ['denuncia', 'acao', 'data_acao', 'usuario']
    
    fieldsets = (
        ('Log da Denúncia', {
            'fields': ('denuncia', 'acao', 'data_acao', 'usuario')
        }),
    )