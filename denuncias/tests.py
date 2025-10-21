from django.test import TestCase
from django.urls import reverse
from .models import Categoria, Denuncia

class DenunciaModelTestCase(TestCase):
    
    def test_protocolo_e_status_padrao(self):
        """Verifica se o protocolo é gerado e o status é 'Pendente' ao salvar."""
        denuncia = Denuncia.objects.create(
            categoria=Categoria.objects.create(nome="Teste"),
            descricao="Teste de protocolo"
        )
        self.assertIsNotNone(denuncia.protocolo)
        self.assertEqual(denuncia.protocolo.length, 6) # Assumindo 6
        self.assertEqual(denuncia.status, 'Pendente')

class DenunciaViewsTestCase(TestCase):
    
    def setUp(self):
        # Cria uma categoria pai e filha
        self.cat_pai = Categoria.objects.create(nome="Iluminação")

    def test_home_view_status_code(self):
        """Verifica se a página inicial (home) carrega."""
        url = reverse('denuncias:home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_denuncia_create_view_post_sucesso(self):
        """Verifica se uma denúncia pode ser criada com sucesso."""
        url = reverse('denuncias:denuncia-create')
        data = {
            'categoria_pai': self.cat_pai.id,
            'categoria': self.cat_filha.id,
            'descricao': 'Poste na rua X'
        }
        response = self.client.post(url, data)
        
        # Verifica se a denúncia foi criada
        self.assertEqual(Denuncia.objects.count(), 1)
        denuncia = Denuncia.objects.first()
        
        # Verifica se o redirecionamento foi para a página de sucesso
        self.assertRedirects(response, reverse('denuncias:denuncia-success', args=[denuncia.protocolo]))

    def test_api_get_subcategories(self):
        """Verifica se a API de subcategorias retorna os dados corretos."""
        url = reverse('denuncias:get-subcategories')
        response = self.client.get(url, {'parent_id': self.cat_pai.id})
        
        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        self.assertEqual(len(json_response), 1)
        self.assertEqual(json_response[0]['nome'], 'Lâmpada Queimada')