# 2. Modelagem UML

## 2.1. Diagrama de Casos de Uso

* **Atores:**
    * `Cidadão` (Anônimo)
    * `Administrador` (Autenticado)
* **Casos de Uso:**
    * `Registrar Denúncia` (Iniciado pelo Cidadão, inclui `Selecionar Categoria` e `Selecionar Subcategoria`)
    * `Consultar Status da Denúncia` (Iniciado pelo Cidadão)
    * `Fazer Login` (Iniciado pelo Administrador)
    * `Gerenciar Denúncias` (Iniciado pelo Administrador)
        * (Estende `Visualizar Denúncias` e `Atualizar Status da Denúncia`)
    * `Gerenciar Categorias` (Iniciado pelo Administrador)
        * (Estende `Criar Categoria/Subcategoria`, `Editar`, `Excluir`)

## 2.2. Diagrama de Classes

Representação dos principais *models* do Django:

```bash
+---------------------+ | Categoria | +---------------------+ | - nome: CharField | | - parent: ForeignKey| +---------------------+ | + str() | +---------------------+ | (parent) | *| +-------V-------------+ | Denuncia | +---------------------+ | - protocolo: CharField (PK) | - descricao: TextField| | - data_criacao: DateTimeField | - status: CharField | | - categoria: ForeignKey(Categoria) +---------------------+ | + save() | | + str() | | + generate_protocol_code() +---------------------+
```
![Diagrama de Classes](./docs/assets/diagrama-classes.png)

## 2.3. Diagrama de Sequência (Registrar Denúncia)

1.  **Cidadão** -> **Navegador**: Preenche o `denuncia_form.html` e clica em "Enviar".
2.  **Navegador** -> **Django (View)**: Envia `POST` para `denuncia_create_view`.
3.  **denuncia_create_view** -> **DenunciaForm**: Instancia o formulário com dados do `POST`.
4.  **denuncia_create_view** -> **DenunciaForm**: Chama `form.is_valid()`.
5.  **denuncia_create_view** -> **DenunciaForm**: Chama `form.save()`.
6.  **DenunciaForm** -> **Denuncia (Model)**: Chama o método `save()` do model.
7.  **Denuncia (Model)** -> **Denuncia (Model)**: Chama `generate_protocol_code()` (se `protocolo` for nulo).
8.  **Denuncia (Model)** -> **Banco de Dados**: `INSERT INTO denuncias (...)`.
9.  **denuncia_create_view** -> **Navegador**: Retorna `redirect` para `denuncia_success_view`.
10. **Navegador** -> **Django (View)**: Envia `GET` para `denuncia_success_view` com o protocolo.
11. **denuncia_success_view** -> **Navegador**: Renderiza `denuncia_success.html` exibindo o protocolo.
