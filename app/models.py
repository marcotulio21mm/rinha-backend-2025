from pydantic import BaseModel
from uuid import UUID

class PaymentRequest(BaseModel): 
    correlationId: UUID
    amount: float

class ProcessorSummary(BaseModel):
    totalRequests: int
    totalAmount: float 

class PaymentsSummary(BaseModel):
    default: ProcessorSummary
    fallback: ProcessorSummary

class HealthResponse(BaseModel):
    failing: bool
    minResponseTime: int