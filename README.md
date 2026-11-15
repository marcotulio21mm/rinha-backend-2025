# Rinha de Backend 2025

Backend intermediário de pagamentos para a [Rinha de Backend 2025](https://github.com/zanfranceschi/rinha-de-backend-2025).

## Stack

- **FastAPI** + Uvicorn
- **Redis** (fila e persistência)
- **nginx** (load balancer)
- Docker Compose

## Arquitetura

```text
Cliente → nginx:9999 → api-1 / api-2 → Redis
                              ↓
              payment-processor-default / fallback
```

Duas instâncias da API ficam atrás do nginx. O estado compartilhado (fila, pagamentos processados e health dos processors) fica no Redis.

### Endpoints

| Método | Path | Descrição |
| --- | --- | --- |
| `POST` | `/payments` | Recebe um pagamento para processamento |
| `GET` | `/payments-summary` | Resumo dos pagamentos processados (`default` / `fallback`) |

Exposto em `http://localhost:9999`.

### Limites de recursos

Total declarado no `docker-compose.yml`: **1.5 CPU** e **350MB** de memória.

## Como rodar

### 1. Payment Processors

Os processors oficiais precisam subir antes do backend (eles criam a rede `payment-processor`):

```bash
cd rinha-de-backend-2025/payment-processor
docker compose up -d
```

- Default: `http://localhost:8001`
- Fallback: `http://localhost:8002`

### 2. Backend

Na raiz deste repositório:

```bash
docker compose up --build -d
```

> É necessário um `Dockerfile` da API na raiz do projeto antes do build.

### 3. Testes locais

Com [k6](https://grafana.com/docs/k6/latest/set-up/install-k6/) instalado:

```bash
cd rinha-de-backend-2025/rinha-test
k6 run rinha.js
```

## Referências

- [Instruções oficiais](https://github.com/zanfranceschi/rinha-de-backend-2025/blob/main/INSTRUCOES.md)
- Clone local do desafio em [`rinha-de-backend-2025/`](./rinha-de-backend-2025/) (processors e scripts de teste)
