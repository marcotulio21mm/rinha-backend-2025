import json
import httpx
import os

from app.models import HealthResponse

DEFAULT_URL = os.getenv("PROCESSOR_DEFAULT_URL", "http://localhost:8001")
FALLBACK_URL = os.getenv("PROCESSOR_FALLBACK_URL", "http://localhost:8002")

def send_payment(payment: dict) -> bool:
    payload = {
        "correlationId": payment['correlationId'],
        "amount": payment['amount'],
        'requestedAt': payment['requestedAt']
    }
    with httpx.Client(timeout=10.0) as client:
        response = client.post(f"{DEFAULT_URL}/payments", json=payload)
        return response.status_code == 200

def get_service_health(url: str) -> HealthResponse:
    with httpx.Client(timeout=5.0) as client:
        response = client.get(url)
        return HealthResponse.model_validate_json(response.text)
        