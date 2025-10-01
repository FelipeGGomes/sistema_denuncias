from django import forms
from .models import Denuncia, Categoria

class DenunciaForm(forms.ModelForm):
   
    titulo = forms.CharField(
        max_length=200,
        label='Título da Denúncia',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ex: Buraco na Rua Principal',
            'class': 'form-control required-field' # Aplicando a classe aqui
        })
    )
    
    # Campo 'localizacao' (usado para preencher o campo 'endereco' no modelo)
    localizacao = forms.CharField(
        max_length=255,
        label='Localização',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ex: Rua das Flores, 123 - Centro',
            'class': 'form-control required-field' # Aplicando a classe aqui
        })
    )
    
    ponto_referencia = forms.CharField(
        max_length=255,
        label='Ponto de Referência',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ex: Próximo ao metrô',
            'class': 'form-control required-field' # Aplicando a classe aqui
        })
    )
    
    class Meta:
        model = Denuncia
        # Incluímos os campos extras (titulo, localizacao) e os campos do modelo (categoria, contato, descricao)
        # Nota: Não incluímos 'endereco' pois será preenchido pelo 'localizacao' no save().
        fields = ['titulo', 'categoria', 'localizacao','ponto_referencia', 'contato', 'descricao']
        
        widgets = {
            'descricao': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Descreva detalhadamente o problema...',
                'class': 'form-control required-field' # Aplicando a classe aqui
            }),
            'contato': forms.TextInput(attrs={
                'placeholder': 'Telefone ou E-mail',
                'class': 'form-control'
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-control required-field', # Aplicando a classe aqui
                'id': 'id_categoria'
            }),
            
            'ponto_referencia': forms.TextInput(attrs={
                'placeholder': 'Ex: Próximo ao metrô',
                'class': 'form-control required-field' # Aplicando a classe aqui
            }),
            # Não é necessário redefinir 'titulo' e 'localizacao' aqui pois já foram definidos acima.
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['categoria'].queryset = Categoria.objects.filter(ativo=True).order_by('nome')
        self.fields['categoria'].empty_label = "Selecione uma categoria"
        
   
        self.fields['contato'].required = False 
        

    # 4. Lógica de Salvamento (Aprimorada)
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        titulo = self.cleaned_data.get('titulo')
        descricao = self.cleaned_data.get('descricao')
        localizacao = self.cleaned_data.get('localizacao')
        
        # Combina Título e Descrição no campo 'descricao' do modelo
        if titulo and descricao:
            instance.descricao = f"{descricao}"
        elif titulo:
            instance.descricao = titulo
            
        # Mapeia 'localizacao' do formulário para 'endereco' do modelo
        instance.endereco = localizacao
        
        # Salva o arquivo (se estiver sendo enviado)
        if self.instance.pk is None and self.files:
             # Se for um novo objeto e houver arquivo, o ModelForm salva o arquivo
             pass # O super().save(commit=False) já preparou a instância para o arquivo.
        
        if commit:
            instance.save()
            
            # Se você tiver campos FileField ou ImageField, eles são salvos aqui
            self.save_m2m() # Importante para ModelForms
            
        return instance

class DenunciaSearchForm(forms.Form):
    protocolo = forms.CharField(
        max_length=20,
        label='Número do Protocolo',
        widget=forms.TextInput(attrs={
            'placeholder': 'Ex: DEN-2023-12345',
            'class': 'form-control protocolo-input',
            'id': 'protocolo-input'
        })
    )

class AdminDenunciaUpdateForm(forms.ModelForm):
    titulo = forms.CharField(
        max_length=200,
        label='Título da Denúncia',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )
    
    localizacao = forms.CharField(
        max_length=255,
        label='Localização',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )
    
    resolucao = forms.CharField(
        required=False,
        label='Resolução do Problema',
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'Descreva como o problema foi resolvido...',
            'class': 'form-control'
        })
    )
    
    data_previsao = forms.DateField(
        required=False,
        label='Previsão de Resolução',
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )
    
    class Meta:
        model = Denuncia
        fields = [
            'titulo', 'categoria', 'localizacao', 'status', 'prioridade', 
            'contato', 'resolucao', 'data_previsao'
        ]
        widgets = {
            'descricao': forms.Textarea(attrs={
                'rows': 4, 
                'class': 'form-control',
                'placeholder': 'Descrição detalhada do problema...'
            }),
            'contato': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-control'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'prioridade': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Carrega todas as categorias
        self.fields['categoria'].queryset = Categoria.objects.all().order_by('nome')
        
        # Preenche os campos titulo e localizacao com dados existentes
        if self.instance and self.instance.pk:
            # Extrai o título da descrição (primeira linha)
            descricao_lines = self.instance.descricao.split('\n')
            if descricao_lines:
                self.fields['titulo'].initial = descricao_lines[0]
            
            # Preenche a localização
            if self.instance.endereco:
                self.fields['localizacao'].initial = self.instance.endereco

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Atualiza a descrição com título e descrição existente
        titulo = self.cleaned_data.get('titulo')
        descricao_existente = instance.descricao
        
        if titulo:
            # Remove o título antigo e mantém o restante da descrição
            lines = descricao_existente.split('\n')
            if len(lines) > 1:
                nova_descricao = f"{titulo}\n\n" + '\n'.join(lines[2:]) if len(lines) > 2 else titulo
            else:
                nova_descricao = titulo
            instance.descricao = nova_descricao
        
        # Atualiza o endereço
        instance.endereco = self.cleaned_data.get('localizacao')
        
        if commit:
            instance.save()
        return instance

class TecnicoLoginForm(forms.Form):
    usuario = forms.CharField(
        max_length=100,
        label='Usuário',
        widget=forms.TextInput(attrs={
            'placeholder': 'Seu usuário',
            'class': 'form-control',
            'id': 'usuario-input'
        })
    )
    senha = forms.CharField(
        max_length=100,
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Sua senha',
            'class': 'form-control',
            'id': 'senha-input'
        })
    )

class DenunciaUpdateStatusForm(forms.ModelForm):
    observacao = forms.CharField(
        required=False,
        label='Observação',
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'Adicione uma observação sobre a atualização...',
            'class': 'form-control'
        })
    )
    
    class Meta:
        model = Denuncia
        fields = ['status', 'prioridade', 'observacao']
        widgets = {
            'status': forms.Select(attrs={
                'class': 'form-control status-select'
            }),
            'prioridade': forms.Select(attrs={
                'class': 'form-control prioridade-select'
            }),
        }

class DenunciaFilterForm(forms.Form):
    # 1. Defina as Choices estáticas normalmente
    STATUS_CHOICES = [
        ('', 'Todos os status'),
    ] + Denuncia.STATUS_CHOICES
    
    # 2. Defina os campos, mas use choices vazias ou placeholder para os campos dinâmicos
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=False,
        label='Status',
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    categoria = forms.ChoiceField(
        choices=[], # Deixe vazio aqui
        required=False,
        label='Categoria',
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    data_inicio = forms.DateField(
        required=False,
        label='Data Início',
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )
    
    data_fim = forms.DateField(
        required=False,
        label='Data Fim',
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )

    # 3. Adicione o método __init__ para carregar as opções dinâmicas
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # AQUI é onde a consulta ao banco de dados deve ocorrer
        try:
            categorias = Categoria.objects.all()
            CATEGORIA_CHOICES = [
                ('', 'Todas as categorias'),
            ] + [(cat.id, cat.nome) for cat in categorias]
            
            # Atribui as choices ao campo
            self.fields['categoria'].choices = CATEGORIA_CHOICES
        
        except Exception:
            # Em caso de erro (como a tabela não existir durante a migração),
            # o formulário usará as choices vazias, permitindo que o comando
            # de migração seja concluído.
            self.fields['categoria'].choices = [('', 'Todas as categorias')]