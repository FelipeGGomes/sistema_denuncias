# 1. Documento de Requisitos

## 1.1. Personas (Perfis de Usuário)

* **Cidadão (Usuário Anônimo):** Morador da comunidade que presencia um problema (ex: lâmpada queimada, atividade suspeita) e deseja reportá-lo de forma segura, rápida e sem se identificar. Seu principal objetivo é ser ouvido e acompanhar a resolução.
* **Administrador (Moderador):** Membro da gestão (ex: prefeitura, associação de bairro) responsável por analisar, triar e atualizar o status das denúncias. Seu objetivo é validar as informações, descartar spam e encaminhar os problemas para as equipes responsáveis.

## 1.2. Histórias de Usuário
```bash
| ID | Persona | História de Usuário |
| :--- | :--- | :--- |
| US01 | Cidadão | Eu, como cidadão, quero poder registrar uma denúncia anônima para informar um problema sem medo de retaliação. |
| US02 | Cidadão | Eu, como cidadão, quero poder selecionar uma categoria principal (ex: "Iluminação Pública"). |
| US03 | Cidadão | Eu, como cidadão, quero que, ao selecionar uma categoria, um segundo campo mostre apenas as subcategorias relacionadas (ex: "Lâmpada Queimada"). |
| US04 | Cidadão | Eu, como cidadão, quero poder descrever o problema em um campo de texto. |
| US05 | Cidadão | Eu, como cidadão, quero receber um código de protocolo curto e único ao final do registro para poder acompanhar o status da minha denúncia. |
| US06 | Cidadão | Eu, como cidadão, quero poder inserir meu código de protocolo em uma página de consulta para ver o status atual da minha denúncia (Pendente, Em Análise, Resolvido). |
| US07 | Admin | Eu, como administrador, quero poder me logar em um painel seguro para gerenciar as denúncias. |
| US08 | Admin | Eu, como administrador, quero ver uma lista de todas as denúncias, podendo filtrar por status ou categoria. |
| US09 | Admin | Eu, como administrador, quero poder abrir uma denúncia específica e alterar seu status. |
| US10 | Admin | Eu, como administrador, quero poder criar, editar e excluir as categorias e subcategorias que aparecem no formulário do cidadão. |
```

## 1.3. Requisitos Funcionais (RF)

* **RF01:** O sistema deve permitir o registro de uma denúncia sem exigir qualquer tipo de login ou identificação do usuário.
* **RF02:** O formulário de denúncia deve conter um campo de seleção de Categoria (principal) e um campo de seleção de Subcategoria (dependente).
* **RF03:** O campo de Subcategoria deve ser preenchido dinamicamente (via JavaScript) com base na Categoria selecionada.
* **RF04:** O sistema deve gerar um código de protocolo alfanumérico, curto (6-10 caracteres) e único para cada denúncia registrada.
* **RF05:** O sistema deve exibir o protocolo gerado em uma página de sucesso após o envio da denúncia.
* **RF06:** O sistema deve possuir uma página pública para consulta de status da denúncia mediante a inserção do protocolo.
* **RF07:** O sistema deve possuir uma área administrativa (`/admin/`) protegida por login e senha.
* **RF08:** O administrador deve poder alterar o status de uma denúncia (Pendente, Em Análise, Resolvido).
* **RF09:** O administrador deve poder gerenciar (CRUD) as Categorias e Subcategorias (estrutura hierárquica `parent`).

## 1.4. Requisitos Não Funcionais (RNF)

* **RNF01 (Anonimato):** O sistema não deve registrar o endereço IP do denunciante ou qualquer outra informação de identificação.
* **RNF02 (Usabilidade):** O formulário de registro deve ser simples e intuitivo.
* **RNF03 (Desempenho):** A consulta de protocolo e o carregamento das subcategorias devem retornar um resultado em menos de 2 segundos.
* **RNF04 (Compatibilidade):** O sistema deve ser responsivo e funcionar em navegadores modernos (desktops e dispositivos móveis).
* **RNF05 (Tecnologia):** O sistema deve ser desenvolvido utilizando Python, o framework Django e templates renderizados no servidor (Django Templates).