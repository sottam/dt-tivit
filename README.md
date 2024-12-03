# dt-tivit

Este projeto foi desenvolvido como parte de um processo seletivo, com o objetivo de demonstrar habilidades em desenvolvimento backend e manipulação de dados.

## Visão Geral

Este backend consome uma API externa de exemplo. Utiliza Django com Celery para processamento assíncrono. O Celery é inicializado automaticamente com a aplicação e consome os dados dessa API para armazená-los no banco de dados local, a partir de onde serão acessados no endpoint `/api/data`.

Devido à natureza assíncrona do Celery, pode levar até 1 minuto para que o banco de dados local seja preenchido com os dados obtidos da API de exemplo. Por favor, aguarde até que o processo seja concluído.

## Instalação e Configuração

### Pré-requisitos

Certifique-se de ter os seguintes pré-requisitos instalados:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### Passos para Instalação

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/seu-usuario/dt-tivit.git
   cd dt-tivit
   ```

2. **Construa e inicie os contêineres:**

   Use Docker Compose para construir as imagens e iniciar os contêineres:

   ```bash
   docker-compose up --build
   ```

A aplicação estará acessível em `http://localhost:8080/` e pronta para ser testada.

## Endpoints

### 1. `POST /api/token/`
Obtém um token JWT a partir de dados de autenticação Basic Auth.

Quando completamente inicializado, um usuário e senha com acesso à API e ao Painel serão gerados com os seguintes usuário e senha:

username: admin
password: admin123

ps.: O header abaixo é a versão em base64 das credenciais acima.

**Headers:**

```http
Authorization: Basic YWRtaW46YWRtaW4xMjM=
```

**Exemplo de resposta:**

```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczMzMzNjE4MSwiaWF0IjoxNzMzMjQ5NzgxLCJqdGkiOiJmNTM5MmFjMWExZmE0ZGQ3OTU5ODJlZGQzNTU1NDE0MiIsInVzZXJfaWQiOjN9.jle6LJNvlwtSJayEPYQMGE1tfi1pu4ez4eVO1ku1r_U",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMzMjUwMDgxLCJpYXQiOjE3MzMyNDk3ODEsImp0aSI6IjQ3MTUxNzU4OTYzNzRiZmQ5YzE0ZWFjZjZlN2UxNDk3IiwidXNlcl9pZCI6M30.Cpvyn7FDLtJpvVZdj1vpbGkMYGuR5S6jZ-SVjVaCgew"
}
```

### 2. `GET /api/data/`
Obtém todos os dados consumidos da API externa em formato JSON.

**Headers:**

```http
Authorization: Bearer <token>
```

**Exemplo de resposta:**

```json
{
    "users": [
        {
            "id": 1,
            "name": "John Doe",
            "email": "john@example.com",
            "user_type": "user",
            "reports": [],
            "purchases": [
                {
                    "id": 1,
                    "item": "Laptop",
                    "price": 2500.0
                },
                {
                    "id": 2,
                    "item": "Smartphone",
                    "price": 1200.0
                }
            ]
        },
        {
            "id": 2,
            "name": "Admin Master",
            "email": "admin@example.com",
            "user_type": "admin",
            "reports": [
                {
                    "id": 1,
                    "title": "Monthly Sales",
                    "status": "Completed"
                },
                {
                    "id": 2,
                    "title": "User Activity",
                    "status": "Pending"
                }
            ],
            "purchases": []
        }
    ]
}
```

## Observações

- O painel de administração do Django está disponível em `/admin`. Você pode acessá-lo para visualizar os dados cadastrados no banco e até adicionar novos dados de teste.
- O processo de sincronização com a API externa pode levar até 1 minuto após a inicialização da aplicação.

## Tecnologias Utilizadas

- **Python**
- **Django**
- **Django Rest Framework**
- **Celery**
- **RabbitMQ**
- **PostgreSQL**
