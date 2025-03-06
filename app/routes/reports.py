from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import func
import pandas as pd
import io
from app.services.database import get_db
from app.services.models import Invoice

router = APIRouter()


# Last Week Report
@router.get("/report/last_week/")
async def last_week_report(db: AsyncSession = Depends(get_db)):
    last_week_query = (
        select(Invoice)
        .where(Invoice.created_at >= func.datetime("now", "-7 days"))
    )
    result = db.execute(last_week_query)
    invoices = result.scalars().all()

    return {"invoices": [invoice.__dict__ for invoice in invoices]}


# Summary Report
@router.get("/report/summary/")
async def summary_report(db: AsyncSession = Depends(get_db)):
    summary_query = (
        select(
            func.count(Invoice.id).label("total_invoices"),
            func.sum(Invoice.amount).label("total_amount"),
            func.avg(Invoice.amount).label("average_amount"),
        )
        .where(Invoice.created_at >= func.datetime("now", "-7 days"))
    )

    result = db.execute(summary_query)
    summary = result.fetchone()

    return {
        "total_invoices": summary.total_invoices,
        "total_amount": summary.total_amount,
        "average_amount": summary.average_amount,
    }


# Export CSV Report
@router.get("/report/last_week/csv/")
async def last_week_report_csv(db: AsyncSession = Depends(get_db)):
    last_week_query = (
        select(Invoice)
        .where(Invoice.created_at >= func.datetime("now", "-7 days"))
    )
    result = db.execute(last_week_query)
    invoices = result.scalars().all()

    if not invoices:
        return {"message": "No invoices found for the last week"}

    # Convert to DataFrame
    df = pd.DataFrame([invoice.__dict__ for invoice in invoices])

    # Convert DataFrame to CSV in-memory
    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)

    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=last_week_report.csv"},
    )
