from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.services.models import Invoice
from app.services.schemas import InvoiceCreate, InvoiceUpdate
from app.services.database import get_db

router = APIRouter()

# Create Invoice
@router.post("/invoice/")
async def create_invoice(invoice_data: InvoiceCreate, db: AsyncSession = Depends(get_db)):
    invoice = Invoice(**invoice_data.dict())
    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    return {"message": "Invoice added successfully!", "invoice": invoice}

# Get All Invoices
@router.get("/invoices/")
async def get_invoices(db: AsyncSession = Depends(get_db)):
    result = db.execute(select(Invoice))
    invoices = result.scalars().all()
    return {"invoices": invoices}

# Get Single Invoice
@router.get("/invoice/{invoice_id}")
async def get_invoice(invoice_id: int, db: AsyncSession = Depends(get_db)):
    invoice = db.get(Invoice, invoice_id)
    if invoice:
        return {"invoice": invoice}
    raise HTTPException(status_code=404, detail="Invoice not found")

# Update Invoice
@router.put("/invoice/{invoice_id}")
async def update_invoice(invoice_id: int, invoice_data: InvoiceUpdate, db: AsyncSession = Depends(get_db)):
    invoice = db.get(Invoice, invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    for key, value in invoice_data.dict(exclude_unset=True).items():
        setattr(invoice, key, value)

    db.commit()
    db.refresh(invoice)
    return {"message": "Invoice updated successfully!", "invoice": invoice}

# Delete Invoice
@router.delete("/invoice/{invoice_id}")
async def delete_invoice(invoice_id: int, db: AsyncSession = Depends(get_db)):
    invoice = db.get(Invoice, invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    db.delete(invoice)
    db.commit()
    return {"message": "Invoice deleted successfully!"}
