from fastapi import FastAPI, Query, Response, status
from datetime import datetime, timezone
from app.models import PaymentRequest, PaymentsSummary, ProcessorSummary
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

@app.get("/payments-summary")
def payments_summary(
    from_: str | None = Query(None, alias="from"), 
    to: str | None = None,
):
    min_score = "-inf" if from_ is None else datetime.fromisoformat(from_.replace("Z", "+00:00")).timestamp() * 1000
    max_score = "+inf" if to is None else datetime.fromisoformat(to.replace("Z", "+00:00")).timestamp() * 1000

    default_count = redis_client.zcount("payments:default", min_score, max_score)
    fallback_count = redis_client.zcount("payments:fallback", min_score, max_score)
    
    default_amount = 19.90
    return PaymentsSummary(
        default=ProcessorSummary(
            totalRequests=default_count,
            totalAmount=default_count * default_amount,
        ),
        fallback=ProcessorSummary(
            totalRequests=fallback_count,
            totalAmount=fallback_count * default_amount,
        )
    )


@app.post("/payments", status_code=status.HTTP_202_ACCEPTED)
def payment(request: PaymentRequest):
    data = {
        "correlationId": str(request.correlationId),
        "amount": request.amount,
        "requestedAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }
    redis_client.lpush("payments:queue", json.dumps(data))
    return Response(status_code=status.HTTP_202_ACCEPTED)

