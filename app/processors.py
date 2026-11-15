import httpx
import os

DEFAULT_URL = os.getenv("PROCESSOR_DEFAULT_URL", "http://localhost:8001")

def send_payment(payment: dict) -> bool:
    payload = {
        "correlationId": payment['correlationId'],
        "amount": payment['amount'],
        'requestedAt': payment['requestedAt']
    }
    with httpx.Client(timeout=10.0) as client:
        response = client.post(f"{DEFAULT_URL}/payments", json=payload)
        return response.status_code == 200