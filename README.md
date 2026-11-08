# Linux Server Monitor

API REST para monitoramento de servidores Linux, desenvolvida como trabalho avaliativo da disciplina de Manutenção de Software.

O projeto permite cadastrar servidores, receber métricas de utilização de recursos e registrar incidentes automaticamente quando determinados limites são ultrapassados.

## Tecnologias utilizadas

- Python 3.11
- Django 4.2
- Django REST Framework
- SQLite
- psutil
- Requests
- Pytest

## Funcionalidades

- Cadastro, consulta, atualização e exclusão de servidores.
- Recebimento e armazenamento de métricas de monitoramento.
- Coleta automática de CPU, memória RAM, disco e uptime por meio de um agente Python.
- Atualização do status do servidor após o recebimento de métricas.
- Criação automática de incidentes quando CPU ou RAM ultrapassam 90%, ou quando o uso de disco ultrapassa 90%.
- Validação dos valores recebidos pela API.

## Estrutura do projeto

```text
django-quickproject/
├── agent/
│   └── monitor.py
├── config/
│   ├── settings.py
│   └── urls.py
├── servers/
│   ├── api/
│   │   ├── serializers.py
│   │   └── views.py
│   ├── migrations/
│   ├── models.py
│   ├── admin.py
│   └── tests.py
├── users/
├── manage.py
├── pytest.ini
└── requirements.txt
```

## Instalação

Clone o repositório e entre no diretório:

```bash
git clone git@github.com:Ataky-0/linux-server-monitor.git
cd linux-server-monitor
```

Crie e ative um ambiente virtual:

```bash
python3.11 -m venv venv
source venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute as migrações do banco de dados:

```bash
python manage.py migrate
```

## Execução da API

Inicie o servidor Django:

```bash
python manage.py runserver
```

A API estará disponível em:

```text
http://127.0.0.1:8000/
```

Para acessar a interface administrativa, crie um superusuário:

```bash
python manage.py createsuperuser
```

Depois acesse:

```text
http://127.0.0.1:8000/admin/
```

## Cadastro de servidor

Antes de executar o agente, cadastre um servidor pela interface da API:

```text
POST http://127.0.0.1:8000/servers/
```

Exemplo de corpo JSON:

```json
{
    "name": "Servidor Linux",
    "hostname": "localhost",
    "ip_address": "127.0.0.1",
    "operating_system": "Arch Linux",
    "status": "offline"
}
```

Anote o ID retornado pela API. Ele será utilizado pelo agente para identificar o servidor monitorado.

## Agente de monitoramento

Com a API em execução e o servidor cadastrado, configure o identificador do servidor em `agent/monitor.py`, na variável `SERVER_ID`.

Execute o agente em outro terminal, dentro do ambiente virtual:

```bash
python -m agent.monitor
```

O agente coleta informações do sistema Linux e envia as métricas à API a cada 30 segundos.

As informações coletadas são:

- Uso de CPU (%).
- Uso de memória RAM (%).
- Uso de disco (%).
- Tempo de atividade do sistema (uptime).

## Endpoints disponíveis

| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/servers/` | Lista servidores |
| POST | `/servers/` | Cadastra servidor |
| GET | `/servers/{id}/` | Consulta servidor |
| PUT/PATCH | `/servers/{id}/` | Atualiza servidor |
| DELETE | `/servers/{id}/` | Exclui servidor |
| GET | `/metrics/` | Lista métricas |
| POST | `/metrics/` | Registra métricas |
| GET | `/incidents/` | Lista incidentes |
| POST | `/incidents/` | Registra incidente |

## Testes automatizados

Para executar os testes:

```bash
pytest -v
```

Os testes verificam o cadastro, a consulta e a atualização de servidores, a rejeição de métricas inválidas e a criação automática de incidentes.

## Banco de dados

O projeto utiliza SQLite, configurado pelo Django. O arquivo do banco de dados é criado localmente durante a execução das migrações e não é versionado no Git.

## Autores

Projeto desenvolvido para a disciplina de Manutenção de Software, da Universidade Federal Rural do Semi-Árido (UFERSA).
