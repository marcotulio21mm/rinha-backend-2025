from fastapi import FastAPI, Response, status
from datetime import datetime, timezone
from app.models import PaymentRequest
from app.redis_client import redis_client
from contextlib import asynccontextmanager
from app.worker import process_queue

import asyncio
import json

@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(process_queue())
    yield
    task.cancel()
    
app = FastAPI(lifespan=lifespan)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/payments", status_code=status.HTTP_202_ACCEPTED)
def payment(request: PaymentRequest):
    data = {
        "correlationId": str(request.correlationId),
        "amount": request.amount,
        "requestedAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }
    redis_client.lpush("payments:queue", json.dumps(data))
    return Response(status_code=status.HTTP_202_ACCEPTED)

