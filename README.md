# Brain Agriculture – Teste Técnico (Back-end)

Aplicação Django/DRF para gestão de produtores rurais, propriedades, safras e culturas. O projeto foi construído para atender aos requisitos do teste técnico da Brain Agriculture e prioriza boas práticas (arquitetura em camadas, validações de domínio, testes automatizados e observabilidade por meio de logs e métricas derivadas).

## Sumário

1. [Arquitetura & Tecnologias](#arquitetura--tecnologias)
2. [Requisitos de Negócio Atendidos](#requisitos-de-negócio-atendidos)
3. [Modelagem e Fluxos Principais](#modelagem-e-fluxos-principais)
4. [Execução com Docker](#execução-com-docker)
5. [Variáveis de Ambiente](#variáveis-de-ambiente)
6. [Testes Automatizados](#testes-automatizados)
7. [Autenticação e Observabilidade](#autenticação-e-observabilidade)
8. [Documentação](#documentação)
9. [Principais Endpoints](#principais-endpoints)

## Arquitetura & Tecnologias

- **Linguagem/Framework**: Python 3.11, Django 4.2, Django REST Framework, SimpleJWT.
- **Banco de Dados**: PostgreSQL 16 (via Docker).
- **Bibliotecas de apoio**: `django-filter`, `drf-spectacular` (OpenAPI/Swagger), `factory-boy` e `pytest` para testes, `django-filter` e `rest_framework.pagination` para filtros/paginação.
- **Infraestrutura local**: Dockerfile + docker-compose sobem PostgreSQL e o app Django. O script `setup_dev.sh` aplica migrações, cria o superusuário, popula o banco com dados e inicia o servidor.
- **Observabilidade**: Configuração de `LOGGING` no `settings.py` envia logs estruturados para o console e instrumentação em ViewSets/Dashboard registra cada operação CRUD relevante.

## Requisitos de Negócio Atendidos

1. CRUD completo de produtores com validação de CPF/CNPJ e normalização do documento (`producers`).
2. Cada produtor (usuário) possui 0..N fazendas; cada fazenda valida as áreas agricultáveis/vegetação (`farm`).
3. Culturas, safras e o relacionamento fazenda+safra+cultura foram modelados com integridade de dados (unicidade e regras de negócio) (`cultivation`).
4. Dashboard autenticado apresenta: total de fazendas, hectares totais, gráfico por estado, por cultura e uso do solo (`brain_agriculture/views.py` + templates em `core/templates`).
5. API REST segura exposta via JWT, com paginação, filtros e openapi.
6. Logs e testes (unitários/integrados) cobrem os casos de uso principais.

## Modelagem e Fluxos Principais

| Entidade | Descrição |
| --- | --- |
| `Producer` | Produtor associado 1:1 ao `User`. Mantém documento único e validado. |
| `Farm` | Propriedade com validação de áreas e vínculo ao produtor (ForeignKey). |
| `Crop` | Cultura agrícola registrada de forma única. |
| `HarvestSeason` | Safra (nome + intervalo de anos) com validação de ordem cronológica. |
| `FarmCrop` | Relação N:N (fazenda × safra × cultura) com restrição de unicidade. |

Fluxos implementados:

- **Signup** – `POST /api/auth/signup/` cria `User` + `Producer` em transação única, já retorna tokens JWT.
- **Autorização** – Todas as rotas de negócios exigem bearer token; usuários comuns só enxergam seus próprios dados.
- **Dashboard Web** – Accessível via `/` (Django Template + Chart.js) após login tradicional.
- **Documentação automática** – `/api/schema/` (OpenAPI JSON) e `/api/docs/` (Swagger UI) via drf-spectacular.

Usuário padrão (Docker): `admin / admin` (definido em `docker-compose.yml`).

## Execução com Docker

```bash
docker-compose up --build
# Banco Postgres sobe automaticamente.
# O serviço django executa setup_dev.sh -> migrações, superuser, popula banco, runserver
```

O backend ficará disponível em `http://localhost:8000`.

## Variáveis de Ambiente

| Variável | Descrição | Default |
| --- | --- | --- |
| `DJANGO_SETTINGS_MODULE` | Módulo de settings | `brain_agriculture.settings` |
| `DJANGO_SUPERUSER_*` | Credenciais automáticas de admin (compose) | `admin` / `admin@admin.com` / `admin` |
| `POSTGRES_*` | Host/porta/credenciais do banco | Definidos no compose (`postgres`) |

## Testes Automatizados

O projeto utiliza `pytest` + `pytest-django`:

```bash
DJANGO_SETTINGS_MODULE=brain_agriculture.settings pytest --disable-warnings -v
# ou via Makefile
make test
```

Há testes de modelos, serializers, views e do fluxo de signup (`core/tests/test_signup.py`). Fábricas em `core/factories.py`, `producers/factories.py`, etc. auxiliam na criação de dados.

## Autenticação e Observabilidade

- **JWT** – use `/api/auth/token/` ou `signup` para obter `access` + `refresh`. Headers: `Authorization: Bearer <access>`.
- **Logs** – Configuração em `brain_agriculture/settings.py` + instrumentação em `core/views.py` e `brain_agriculture/views.py`. Cada criação/atualização/exclusão gera um log no formato `[timestamp] INFO brain_agriculture.api ...` facilitando monitoramento.
- **Permissões** – `IsOwnerOrStaff` garante que usuários comuns só acessem seus recursos. Staff tem visão global.

## documentação

- **OpenAPI JSON**: `GET /api/schema/`
- **Swagger UI**: `GET /api/docs/`


## Principais Endpoints

| Recurso | Método | Caminho | Descrição |
| --- | --- | --- | --- |
| Auth | POST | `/api/auth/signup/` | Cadastro + JWT. |
| Auth | POST | `/api/auth/token/` | Login (username/password). |
| Auth | POST | `/api/auth/token/refresh/` | Refresh token. |
| Produtores | CRUD | `/api/producers/` | Gerenciamento completo com filtros e paginação. |
| Fazendas | CRUD | `/api/farms/` | Validações de área + filtros. |
| Culturas | CRUD | `/api/crops/` | Cadastro de culturas. |
| Safras | CRUD | `/api/harvest-seasons/` | Registro de safra com validação de anos. |
| Farm Crops | CRUD | `/api/farm-crops/` | Associação entre fazenda, safra e cultura (única). |
| Dashboard | GET | `/` + `/login` | Dashboard HTML + autenticação clássica. |

Além das operações básicas, todos os recursos oferecem filtros (`django-filter`) e ordenação (`ordering` query param). Consulte o Swagger para parâmetros detalhados.

---

Qualquer dúvida ou sugestão, fique à vontade para entrar em contato!
