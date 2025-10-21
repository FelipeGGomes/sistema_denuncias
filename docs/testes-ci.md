# 1. Testes e Integração Contínua (CI)

A integração contínua é gerenciada pelo GitHub Actions, conforme definido no arquivo `.github/workflows/django-ci.yml`.

## 1.1. Pipeline de CI (django-ci.yml)

O pipeline é executado em todo `push` para a branch `main`. Ele automatiza os passos de build e teste.

```yaml
# .github/workflows/django-ci.yml
name: Django CI

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11"]

    steps:
      # 1. Clona o repositório
      - name: Checkout repository
        uses: actions/checkout@v3

      # 2. Configura a versão do Python
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v3
        with:
          python-version: ${{ matrix.python-version }}

      # 3. Etapa de "Build"
      - name: Install Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      
      # 4. Etapa de "Testes Automatizados"
      - name: Run Tests
        run: |
          python manage.py test