# 🥗 Daily-Diet-API

API para controle de dieta diária, desenvolvida com Flask + SQLAlchemy + MySQL.

---

## 🚀 Como subir o projeto (modo desenvolvimento)

Suba os serviços com Docker Compose:

```bash
docker-compose up web
```

A API estará disponível em: http://localhost:5000

## 🧪 Rodando os testes

```bash
docker-compose run --rm tests
```

Os testes utilizam um ambiente isolado com variáveis definidas em `.env.testing.`

## 🛠️ Criando as tabelas no banco de dados

Após subir os containers pela primeira vez, execute o seguinte para criar as tabelas:

1. Acesse o shell interativo do Flask:

```bash
docker-compose exec web flask shell
```

2. Dentro do shell, rode:

```bash
from app import db
db.create_all()
```

## 📁 Variáveis de ambiente

* `.env` — usado em desenvolvimento.
* `.env.testing` — usado nos testes.