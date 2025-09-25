import csv
from io import StringIO
from datetime import datetime
from typing import Optional
from sqlmodel import Session, select
from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse, FileResponse
from ..database import get_session
from ..models import Transaction, TokenData
from ..auth import get_current_user
from ..config import get_settings

router = APIRouter(prefix="/api/export", tags=["export"])
settings = get_settings()


@router.get("/csv")
async def export_csv(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    session: Session = Depends(get_session),
    current_user: TokenData = Depends(get_current_user)
):
    query = select(Transaction)
    if start_date:
        query = query.where(Transaction.date >= start_date)
    if end_date:
        query = query.where(Transaction.date <= end_date)

    query = query.order_by(Transaction.date.desc())
    transactions = session.exec(query).all()

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "ID", "Date", "Amount", "Type", "Category",
        "Description", "Created At", "Updated At"
    ])

    for trans in transactions:
        writer.writerow([
            trans.id,
            trans.date.strftime("%Y-%m-%d %H:%M:%S"),
            float(trans.amount),
            trans.type,
            trans.category,
            trans.description or "",
            trans.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            trans.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        ])

    output.seek(0)
    filename = f"nestegg_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@router.get("/database")
async def export_database(
    current_user: TokenData = Depends(get_current_user)
):
    db_path = settings.database_url.replace("sqlite:///", "")
    filename = f"nestegg_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"

    return FileResponse(
        path=db_path,
        filename=filename,
        media_type="application/octet-stream"
    )