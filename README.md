# Sistema de Gestão de Denúncias

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)


## 📜 Sumário

* [Visão Geral](#-visão-geral)
* [Funcionalidades](#-funcionalidades)
* [Tecnologias Utilizadas](#-tecnologias-utilizadas)
* [Pré-requisitos](#-pré-requisitos)
* [Como Executar o Projeto](#-como-executar-o-projeto)
* [Estrutura do Projeto](#-estrutura-do-projeto)
* [Como Contribuir](#-como-contribuir)
* [Licença](#-licença)

## 🚀 Visão Geral

O **Sistema de Gestão de Denúncias** é uma aplicação web completa desenvolvida para permitir que usuários registrem denúncias de forma anônima ou identificada. A plataforma oferece um painel administrativo robusto para que gestores possam visualizar, categorizar, atribuir e acompanhar o andamento de cada denúncia, garantindo uma resolução eficiente e transparente.

## ✨ Funcionalidades

* **Registro de Denúncias:** Formulário público para que qualquer pessoa possa submeter uma denúncia com detalhes, categoria e evidências (upload de arquivos).
* **Acompanhamento por Protocolo:** O usuário recebe um número de protocolo para consultar o status de sua denúncia.
* **Painel Administrativo:** Área restrita para administradores gerenciarem todas as denúncias recebidas.
* **Gestão de Status:** Administradores podem alterar o status de uma denúncia (ex: "Recebida", "Em Análise", "Resolvida", "Arquivada").
* **Sistema de Autenticação:** Controle de acesso para a equipe de gestão.
* **Dashboard com Estatísticas:** [Se houver] Visualização de gráficos com o número de denúncias por categoria, status, etc.

## 🛠️ Tecnologias Utilizadas

Este projeto foi construído inteiramente com o ecossistema Django, aproveitando seu sistema de templates para a renderização do frontend.

* **Linguagem:** Python 3.13.5
* **Framework:** Django
* **Banco de Dados:** [SQLite (padrão de desenvolvimento)]
* **Frontend:** Django Templates, HTML5, CSS3, JavaScript
* **Estilização:** [Bootstrap e CSS]

## ✅ Pré-requisitos

Antes de começar, você vai precisar ter instalado em sua máquina:
* [Git](https://git-scm.com)
* [Python 3.13.5](https://www.python.org/) e `pip`

## ⚙️ Como Executar o Projeto

Siga os passos abaixo para configurar e executar o ambiente de desenvolvimento localmente.

```bash
# 1. Clone o repositório
git clone [https://github.com/FelipeGGomes/sistema_denuncias.git](https://github.com/FelipeGGomes/sistema_denuncias.git)

# 2. Navegue até a pasta do projeto
cd sistema_denuncias

# 3. Crie e ative um ambiente virtual
# No Windows:
python -m venv venv
venv\Scripts\activate
# No Linux/Mac:
python3 -m venv venv
source venv/bin/activate

# 4. Instale as dependências do Python
pip install -r requirements.txt

# 5. Aplique as migrações do banco de dados
python manage.py migrate

# 6. Crie um superusuário para acessar o painel administrativo
python manage.py createsuperuser
# (Siga as instruções no terminal para criar seu usuário e senha)

# 7. Inicie o servidor de desenvolvimento
python manage.py runserver
```

## 📁 Estrutura do Projeto

```bash
.
├── manage.py           # Utilitário de linha de comando do Django
├── requirements.txt    # Lista de dependências Python
├── venv/               # Diretório do ambiente virtual (ignorado pelo Git)
├── .gitignore          # Arquivos e pastas a serem ignorados pelo Git
│
├── sistema_denuncias/  # Diretório principal do projeto Django (configurações)
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── denuncias/          # Exemplo de um app Django para o módulo de denúncias
│   ├── migrations/
│   ├── templates/      # Arquivos HTML do app
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── ...
│
└── static/             # Arquivos estáticos globais (CSS, JS, Imagens)

```

## 🤝 Como Contribuir

Contribuições são muito bem-vindas! Se você tem alguma ideia para melhorar o projeto, sinta-se à vontade para seguir estes passos:

* **Faça um Fork do projeto**
* **Crie uma Branch para sua Feature (git checkout -b feature/NovaFuncionalidade)**
* **Faça o Commit de suas alterações (git commit -m 'Adiciona NovaFuncionalidade')**
* **Faça o Push para a Branch (git push origin feature/NovaFuncionalidade)**
* **Abra um Pull Request**
