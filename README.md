Store API - Desafio DIO
Esta é uma API desenvolvida como parte do desafio da DIO (Digital Innovation One). O objetivo principal do projeto foi aplicar o Desenvolvimento Orientado a Testes (TDD) na prática, utilizando FastAPI para a construção da API, MongoDB para persistência de dados e Pytest para garantir a qualidade e a integridade do código.

📋 Sobre o Projeto
A aplicação permite o gerenciamento de produtos (CRUD) com suporte a filtros, paginação e tratamento robusto de erros. O projeto foi construído focando em uma arquitetura limpa, desacoplada e testável.

🚀 Tecnologias Utilizadas
Linguagem: Python 3.14

Framework: FastAPI

Banco de Dados: MongoDB (Motor)

Validação de Dados: Pydantic v2

Testes: Pytest, Pytest-asyncio, Httpx

Gerenciador de Dependências: Poetry

⚙️ Funcionalidades Implementadas
[x] TDD: Ciclo completo de Red-Green-Refactor com 16 testes de integração.

[x] CRUD Completo: Create, Read, Update, Delete.

[x] Tratamento de Exceções: Handler global para exceções customizadas (ex: NotFoundException).

[x] Paginação e Filtros: Query parameters para paginação e busca por nome.

[x] Conversão de Dados: Suporte nativo a Decimal128 para valores monetários.

[x] Auditoria: Atualização automática do campo updated_at em operações de escrita.

🛠️ Como rodar o projeto
Pré-requisitos
Certifique-se de ter o Poetry instalado.

Passo a passo
Clone este repositório:

Bash
git clone <link-do-seu-repositorio>
cd store_api
Instale as dependências:

Bash
poetry install
Configure as variáveis de ambiente (arquivo .env):

Plaintext
DATABASE_URL=mongodb://localhost:27017/store
Execute os testes para validar o ambiente:

Bash
poetry run pytest -v
Inicie a API:

Bash
poetry run fastapi dev store/main.py
📝 Documentação Automática
Após iniciar a aplicação, acesse a documentação interativa gerada pelo Swagger em:
http://localhost:8000/docs

Desenvolvido por Irivânia Maria de Melo
