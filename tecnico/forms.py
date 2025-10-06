from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

# Opções de status que o técnico pode selecionar
STATUS_CHOICES = [
    ('EM_ANDAMENTO', 'Em Andamento'),
    ('RESOLVIDA', 'Resolvida'),
    ('ARQUIVADA', 'Arquivada'),
]

class UpdateStatusForm(forms.Form):
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        label="Alterar Status Para",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    comentario = forms.CharField(
        label="Adicionar Comentário/Observação (Obrigatório)",
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        help_text="Descreva a ação tomada ou o motivo da alteração de status."
    )
    
class AlterarEmailForm(forms.Form):
    novo_email = forms.EmailField(
        label="Novo E-mail",
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    
    
class AlterarSenhaForm(forms.Form):
    senha_atual = forms.CharField(
        label="Senha Atual",
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    nova_senha = forms.CharField(
        label="Nova Senha",
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    confirmar_senha = forms.CharField(
        label="Confirmar Nova Senha",
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    
    def clean_confirmar_senha(self):
        nova_senha = self.cleaned_data.get("nova_senha")
        confirmar_senha = self.cleaned_data.get("confirmar_senha")
        if nova_senha != confirmar_senha:
            raise ValidationError("As senhas não coincidem.")
        return confirmar_senha