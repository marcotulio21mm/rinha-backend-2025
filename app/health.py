import asyncio
from app.redis_client import redis_client
from app.processors import DEFAULT_URL, FALLBACK_URL, get_service_health

async def poll_health():
    while True:
        try:
            got_lock = redis_client.set("health:lock", "1", nx=True, ex=5)
            if not got_lock:
                continue
            default = await asyncio.to_thread(
                get_service_health,
                f"{DEFAULT_URL}/payments/service-health",
            )
            fallback = await asyncio.to_thread(
                get_service_health,
                f"{FALLBACK_URL}/payments/service-health",
            )
            redis_client.hset("health:default", mapping={
                "failing":"1" if default.failing else "0",
                "minResponseTime": default.minResponseTime
            })
            redis_client.hset("health:fallback", mapping={
                "failing": "1" if fallback.failing else "0",
                "minResponseTime": fallback.minResponseTime
            })
        except Exception as e:
            print("erro no health:", e, flush=True)
        await asyncio.sleep(5)
            

