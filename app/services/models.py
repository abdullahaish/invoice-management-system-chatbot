from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from app.services.database import Base

# SQLAlchemy Invoice Model (DB Table)
class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, index=True)
    amount = Column(Float)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
