from pydantic import BaseModel
from uuid import UUID

class PaymentRequest(BaseModel): 
    correlationId: UUID
    amount: float