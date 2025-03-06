from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import openai
from app.services.database import get_db
from app.services.models import Invoice
from app.services.schemas import ChatRequest, InvoiceUpdate
from app.routes.reports import summary_report
from app.services.config import OPENAI_API_KEY

router = APIRouter()

openai.api_key = OPENAI_API_KEY

# Store Last Invoice ID (Instead of Whole Object)
chat_context = {}

@router.post("/chat/")
async def chat_with_bot(request: ChatRequest, db: AsyncSession = Depends(get_db)):
    user_message = request.message.lower()

    # Retrieve Last Invoice ID (Instead of Object)
    last_invoice_id = chat_context.get("last_invoice_id")

    # Handle Invoice Summary Query
    if "summary of invoices" in user_message:
        return summary_report(db)

    # Fetch Last Invoice if User Asks
    if "show my last invoice" in user_message or "last invoice" in user_message:
        last_invoice_query = select(Invoice).order_by(Invoice.created_at.desc()).limit(1)
        result = db.execute(last_invoice_query)
        last_invoice = result.scalars().first()

        if last_invoice:
            chat_context["last_invoice_id"] = last_invoice.id  # Store ID, Not Object
            return {"invoice": last_invoice.__dict__}
        else:
            return {"message": "No invoices found."}

    # Handle Update Request
    if "update invoice" in user_message:
        if not last_invoice_id:
            return {"message": "Please specify which invoice you want to update."}

        # Re-fetch the Invoice to Ensure It Is Attached to Session
        invoice = db.get(Invoice, last_invoice_id)
        if not invoice:
            return {"message": "Invoice not found."}

        # Simulate an update (In real scenario, parse the user's intent)
        update_data = InvoiceUpdate(status="Paid")
        for key, value in update_data.dict(exclude_unset=True).items():
            setattr(invoice, key, value)

        db.commit()
        db.refresh(invoice)
        return {"message": f"Invoice {invoice.id} updated successfully!", "invoice": invoice.__dict__}

    # Handle Deletion Request
    if "delete invoice" in user_message:
        if not last_invoice_id:
            return {"message": "Please specify which invoice you want to delete."}

        # Re-fetch the Invoice
        invoice = db.get(Invoice, last_invoice_id)
        if not invoice:
            return {"message": "Invoice not found."}

        db.delete(invoice)
        db.commit()
        chat_context.pop("last_invoice_id", None)  # Remove context after deletion
        return {"message": f"Invoice {invoice.id} deleted successfully!"}

    # Default Chatbot Response
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are an invoice management assistant."},
            {"role": "user", "content": request.message}
        ]
    )
    return {"response": response['choices'][0]['message']['content']}
