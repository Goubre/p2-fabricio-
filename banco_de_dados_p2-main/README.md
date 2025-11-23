# TransFlow – Sistema de Processamento de Corridas

Este projeto é um sistema distribuído que utiliza **FastAPI**, **RabbitMQ**, **MongoDB** e **Redis** para processar corridas de motoristas e atualizar saldos em tempo real.

---

## 🚀 Tecnologias Utilizadas

* **Python 3.10+**
* **FastAPI** (API principal)
* **RabbitMQ** (mensageria)
* **Redis** (controle de saldo dos motoristas)
* **MongoDB** (armazenamento das corridas)
* **Docker + Docker Compose**

---

## 📦 Arquitetura

O projeto segue a seguinte arquitetura em containers:

* **api** → recebe dados e envia mensagens para o RabbitMQ
* **consumer** → lê mensagens da fila e processa as corridas
* **mongo** → banco para armazenar as corridas
* **redis** → banco para armazenar saldos por motorista
* **rabbitmq** → sistema de filas

---

## 🛠️ Como Rodar o Projeto

### 1. Crie o arquivo `.env` com as variáveis:

```
MONGO_URI=mongodb://mongo:27018/transflow_db
REDIS_URI=redis://redis:6379/0
RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672/
RABBITMQ_QUEUE=corridas_queue
```

### 2. Suba os containers:

```bash
docker compose up -d
```

### 3. Verifique se os serviços estão no ar:

* API: [http://localhost:8000/docs](http://localhost:8000/docs)
* RabbitMQ: [http://localhost:15672](http://localhost:15672) (guest / guest)
* MongoDB: porta 27018
* Redis: porta 6379

---

## 📤 Envio de Corridas

A API recebe corridas no endpoint:

```
POST /corridas
```

### Exemplo de payload:

```json
{
  "id_corrida": "123",
  "motorista": {
    "nome": "Carlos"
  },
  "valor_corrida": 25.50
}
```

O backend envia esse payload para o RabbitMQ.

---

## 🐇 Consumer – Processamento das Corridas

O consumo funciona assim:

1. Lê a mensagem da fila RabbitMQ
2. Atualiza o saldo no Redis usando **watch + transaction**
3. Salva/atualiza a corrida no MongoDB

---

## 📊 Estrutura no Redis

Chaves criadas:

```
saldo:<nome_do_motorista>
```

Exemplo:

```
saldo:carlos
```

Guarda o saldo acumulado.

---

## 📘 Estrutura no MongoDB

Coleção: `corridas`

Documento salvo:

```json
{
  "id_corrida": "123",
  "motorista": {
    "nome": "Carlos"
  },
  "valor_corrida": 25.50
}
```

---

## 🧪 Testes

Você pode testar direto pelo Swagger em:

```
http://localhost:8000/docs
```

---

## 🐳 Comandos Úteis

### Ver logs:

```
docker logs api -f
docker logs consumer -f
```

### Acessar containers:

```
docker exec -it api sh
docker exec -it consumer sh
```

---

## 📄 Licença

Projeto livre para uso e modificação.
