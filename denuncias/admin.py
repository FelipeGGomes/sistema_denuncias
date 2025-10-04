from django.contrib import admin
from .models import Denuncia, LogDenuncia, Categoria
from django.utils.translation import gettext_lazy as _

# Admin para Categoria
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao', 'ativo', 'ordem', 'denuncias_count')
    search_fields = ('nome',)
    list_filter = ('ativo',)

    def denuncias_count(self, obj):
        return obj.denuncias_count
    denuncias_count.short_description = _('Número de Denúncias')


class DenunciaAdmin(admin.ModelAdmin):
    list_display = ('protocolo', 'titulo', 'categoria', 'status', 'prioridade', 'data_criacao', 'data_resolucao', 'tem_foto', 'tecnico')
    search_fields = ('protocolo', 'titulo', 'descricao', 'endereco')
    list_filter = ('status', 'prioridade', 'categoria', 'data_criacao', 'data_resolucao', 'tecnico')
    readonly_fields = ('protocolo', 'data_criacao', 'data_atualizacao', 'data_resolucao', 'resolucao', 'observacoes_internas')
    
    fieldsets = (
        (None, {
            'fields': ('protocolo', 'titulo', 'descricao', 'endereco', 'ponto_referencia', 'categoria', 'status', 'prioridade', 'contato', 'foto', 'tecnico')
        }),
        (_('Datas Importantes'), {
            'fields': ('data_criacao', 'data_atualizacao', 'data_previsao_resolucao', 'data_resolucao')
        }),
        (_('Campos Administrativos'), {
            'fields': ('resolucao', 'observacoes_internas')
        }),
    )

    def get_status_display_color(self, obj):
        return obj.get_status_display_color()

    def get_prioridade_display_color(self, obj):
        return obj.get_prioridade_display_color()

    get_status_display_color.short_description = _('Cor do Status')
    get_prioridade_display_color.short_description = _('Cor da Prioridade')


class LogDenunciaAdmin(admin.ModelAdmin):
    list_display = ('denuncia', 'tipo_acao', 'acao', 'data_acao', 'usuario')
    search_fields = ('denuncia__protocolo', 'acao', 'descricao')
    list_filter = ('tipo_acao', 'data_acao', 'usuario')
    readonly_fields = ('denuncia', 'tipo_acao', 'acao', 'descricao', 'data_acao', 'usuario', 'dados_anteriores', 'dados_novos')
    
    fieldsets = (
        (None, {
            'fields': ('denuncia', 'tipo_acao', 'acao', 'descricao')
        }),
        (_('Data e Usuário'), {
            'fields': ('data_acao', 'usuario')
        }),
        (_('Dados Anteriores e Novos'), {
            'fields': ('dados_anteriores', 'dados_novos')
        }),
    )

# Registrando no Admin
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Denuncia, DenunciaAdmin)
admin.site.register(LogDenuncia, LogDenunciaAdmin)
