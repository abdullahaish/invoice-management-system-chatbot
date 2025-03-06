from fastapi import FastAPI
from app.routes import invoices, chatbot, reports
from app.services.database import Base, engine

app = FastAPI(title="Invoice Management System with Chatbot")

# Initialize database on startup
Base.metadata.create_all(bind=engine)

# Include API routes
app.include_router(invoices.router, prefix="/api")
app.include_router(chatbot.router, prefix="/api")
app.include_router(reports.router, prefix="/api")

@app.get("/")
def home():
    return {"message": "Welcome to Invoice Management System"}
