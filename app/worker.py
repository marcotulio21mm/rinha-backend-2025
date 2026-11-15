import asyncio
import json
from app.redis_client import redis_client
from app.processors import send_payment
from datetime import datetime

async def process_queue():
    while True:
        try:
            item = await asyncio.to_thread(redis_client.brpop, "payments:queue", 5)
            # brpop devolve None no timeout, ou (chave, valor)
            if item is None:
                continue
            _,raw = item
            payment = json.loads(raw)
            ok = await asyncio.to_thread(send_payment, payment)

            if ok:
                score = datetime.fromisoformat(
                    payment["requestedAt"].replace("Z", "+00:00")
                    ).timestamp() * 1000
                redis_client.zadd(
                    "payments:default", 
                    {payment['correlationId']: score},
                    )
            else:
                redis_client.lpush("payments:queue", json.dumps(payment))
        except Exception as e:
            print("erro no worker:",e, flush=True)
    