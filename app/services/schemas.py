from pydantic import BaseModel
from typing import Optional

# Pydantic Model for Creating Invoices
class InvoiceCreate(BaseModel):
    customer_name: str
    amount: float
    status: str

# Pydantic Model for Updating Invoices (Partial Updates Allowed)
class InvoiceUpdate(BaseModel):
    customer_name: Optional[str] = None
    amount: Optional[float] = None
    status: Optional[str] = None

class ChatRequest(BaseModel):
    message: str