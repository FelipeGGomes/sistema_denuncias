# 3. Arquitetura do Sistema

## 3.1. Arquitetura MVT (Model-View-Template)

O projeto é uma aplicação web monolítica desenvolvida com o framework Django, que segue uma variação da arquitetura MVC conhecida como MVT (Model-View-Template).

* **Model (`models.py`):** Define a estrutura dos dados (as tabelas `Categoria` e `Denuncia`), suas validações e a lógica de negócio associada (como gerar um protocolo no método `save()`).
* **View (`views.py`):** É a camada de lógica que processa as requisições HTTP. Ela busca dados dos *Models*, processa-os (ex: valida um formulário) e decide qual *Template* deve ser renderizado como resposta.
* **Template (`templates/`):** É a camada de apresentação. Consiste em arquivos HTML com tags especiais do Django (`{% ... %}`) que exibem os dados preparados pela *View*.

## 3.2. Estrutura de Arquivos do Projeto

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