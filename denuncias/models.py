import random
import string
from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils import timezone


class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True, null=True, help_text="Descrição opcional da categoria")
    ativo = models.BooleanField(default=True, help_text="Se a categoria está ativa para uso")
    ordem = models.PositiveIntegerField(default=0, help_text="Ordem de exibição da categoria")
    
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['ordem', 'nome']
    
    def __str__(self):
        return self.nome

    @property
    def denuncias_count(self):
        """Retorna o número de denúncias nesta categoria"""
        return self.denuncias.count()


def generate_protocol_code():
    """Gera um código de protocolo único no formato DEN-XXXXXX"""
    length = 6
    characters = string.ascii_uppercase + string.digits
    while True:
        random_part = ''.join(random.choices(characters, k=length))
        code = f"DEN-{random_part}"
        if not Denuncia.objects.filter(protocolo=code).exists():
            return code


class Denuncia(models.Model):
    STATUS_CHOICES = [
        ('NÃO_ATRIBUIDO', 'Aguardando Atribuição'),
        ('RECEBIDA', 'Recebida'),
        ('EM_ANALISE', 'Em Análise'),
        ('EM_ANDAMENTO', 'Em Andamento'),
        ('RESOLVIDA', 'Resolvida'),
        ('ARQUIVADA', 'Arquivada'),
    ]
    
    PRIORIDADE_CHOICES = [
        ('BAIXA', 'Baixa'),
        ('MEDIA', 'Média'),
        ('ALTA', 'Alta'),
        ('URGENTE', 'Urgente'),
    ]

    # Identificação
    protocolo = models.CharField(
        max_length=10, 
        primary_key=True, 
        blank=True, 
        editable=False, 
        unique=True,
        verbose_name="Número do Protocolo"
    )
    
    # Informações básicas
    titulo = models.CharField(
        max_length=200, 
        verbose_name="Título da Denúncia",
        help_text="Título resumido do problema"
    )
    descricao = models.TextField(
        verbose_name="Descrição Detalhada",
        help_text="Descreva o problema em detalhes"
    )
    
    # Localização e categoria
    endereco = models.CharField(
        max_length=255, 
        verbose_name="Localização",
        help_text="Endereço ou local onde ocorreu o problema"
    )
    ponto_referencia = models.CharField(
        max_length=255, 
        blank=True, 
        null=True,
        verbose_name="Ponto de Referência",
        help_text="Ponto de referência próximo (opcional)"
    )
    
    categoria = models.ForeignKey(
        Categoria, 
        on_delete=models.PROTECT, 
        related_name='denuncias',
        verbose_name="Categoria do Problema"
    )

    # Status e prioridade
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='NÃO_ATRIBUIDO',
        verbose_name="Status da Denúncia"
    )
    prioridade = models.CharField(
        max_length=20, 
        choices=PRIORIDADE_CHOICES, 
        default='MEDIA',
        verbose_name="Prioridade"
    )
    
    # Contato (opcional)
    contato = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        verbose_name="Contato",
        help_text="Telefone ou e-mail para retorno (opcional)"
    )
    
    # Mídia - MELHORIAS NA IMAGEM
    foto = models.ImageField(
        upload_to='denuncias/%Y/%m/%d/', 
        blank=True, 
        null=True,
        verbose_name="Foto do Problema",
        help_text="Faça upload de uma foto que mostre o problema",
        validators=[
            FileExtensionValidator(
                allowed_extensions=['jpg', 'jpeg', 'png', 'gif'],
                message="Somente imagens JPG, JPEG, PNG ou GIF são permitidas"
            )
        ]
    )
    
    # Datas importantes
    data_criacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Criação"
    )
    data_atualizacao = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Atualização"
    )
    data_previsao_resolucao = models.DateField(
        blank=True, 
        null=True,
        verbose_name="Previsão de Resolução"
    )
    data_resolucao = models.DateField(
        blank=True, 
        null=True,
        verbose_name="Data de Resolução"
    )
    
    # Campos administrativos
    resolucao = models.TextField(
        blank=True, 
        null=True,
        verbose_name="Solução Aplicada",
        help_text="Descrição de como o problema foi resolvido"
    )
    observacoes_internas = models.TextField(
        blank=True, 
        null=True,
        verbose_name="Observações Internas",
        help_text="Observações para uso da equipe administrativa"
    )

    class Meta:
        verbose_name = 'Denúncia'
        verbose_name_plural = 'Denúncias'
        ordering = ['-data_criacao']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['prioridade']),
            models.Index(fields=['data_criacao']),
            models.Index(fields=['categoria']),
        ]

    def __str__(self):
        return f"Denúncia {self.protocolo} - {self.titulo}"

    def save(self, *args, **kwargs):
        if not self.protocolo:
            self.protocolo = generate_protocol_code()
        
        # Atualiza data de resolução se o status for alterado para RESOLVIDA
        if self.status == 'RESOLVIDA' and not self.data_resolucao:
            self.data_resolucao = timezone.now().date()
        
        super().save(*args, **kwargs)

    @property
    def tempo_decorrido(self):
        """Retorna o tempo decorrido desde a criação da denúncia"""
        return timezone.now() - self.data_criacao

    @property
    def dias_em_aberto(self):
        """Retorna o número de dias que a denúncia está em aberto"""
        return (timezone.now().date() - self.data_criacao.date()).days

    @property
    def tem_foto(self):
        """Verifica se a denúncia possui foto"""
        return bool(self.foto)

    def get_status_display_color(self):
        """Retorna a cor CSS para o status atual"""
        colors = {
            'RECEBIDA': 'info',
            'EM_ANALISE': 'warning',
            'EM_ANDAMENTO': 'primary',
            'RESOLVIDA': 'success',
            'ARQUIVADA': 'secondary',
        }
        return colors.get(self.status, 'secondary')

    def get_prioridade_display_color(self):
        """Retorna a cor CSS para a prioridade atual"""
        colors = {
            'BAIXA': 'success',
            'MEDIA': 'info',
            'ALTA': 'warning',
            'URGENTE': 'danger',
        }
        return colors.get(self.prioridade, 'info')


class LogDenuncia(models.Model):
    TIPO_ACAO_CHOICES = [
        ('CRIACAO', 'Criação'),
        ('ATUALIZACAO', 'Atualização'),
        ('STATUS', 'Alteração de Status'),
        ('PRIORIDADE', 'Alteração de Prioridade'),
        ('RESOLUCAO', 'Resolução'),
        ('COMENTARIO', 'Comentário'),
    ]

    denuncia = models.ForeignKey(
        Denuncia, 
        on_delete=models.CASCADE, 
        related_name='logs'
    )
    tipo_acao = models.CharField(
        max_length=20, 
        choices=TIPO_ACAO_CHOICES,
        verbose_name="Tipo de Ação"
    )
    acao = models.CharField(
        max_length=255,
        verbose_name="Descrição da Ação"
    )
    descricao = models.TextField(
        blank=True, 
        null=True,
        verbose_name="Detalhes da Ação"
    )
    data_acao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data da Ação"
    )
    usuario = models.ForeignKey(
        'auth.User', 
        on_delete=models.SET_NULL, 
        null=True,
        blank=True,
        related_name='logs_denuncias',
        verbose_name="Usuário Responsável"
    )
    
    # Campo para armazenar dados antigos (para auditoria)
    dados_anteriores = models.JSONField(
        blank=True, 
        null=True,
        verbose_name="Dados Anteriores"
    )
    dados_novos = models.JSONField(
        blank=True, 
        null=True,
        verbose_name="Dados Novos"
    )

    class Meta:
        verbose_name = 'Log de Denúncia'
        verbose_name_plural = 'Logs de Denúncias'
        ordering = ['-data_acao']

    def __str__(self):
        return f"Log {self.denuncia.protocolo} - {self.tipo_acao}"


# Signal para criar log automaticamente
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Denuncia)
def criar_log_denuncia(sender, instance, created, **kwargs):
    if created:
        LogDenuncia.objects.create(
            denuncia=instance,
            tipo_acao='CRIACAO',
            acao='Denúncia criada',
            descricao='Denúncia registrada no sistema',
        )