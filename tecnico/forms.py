from django import forms

# Opções de status que o técnico pode selecionar
STATUS_CHOICES = [
    ('EM_ANDAMENTO', 'Marcar como "Em Andamento"'),
    ('RESOLVIDA', 'Marcar como "Resolvida"'),
    ('ARQUIVADA', 'Marcar como "Arquivada"'),
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