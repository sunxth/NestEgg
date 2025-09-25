from typing import List, Optional
from datetime import datetime, timedelta
from sqlmodel import Session, select, func, and_
from fastapi import APIRouter, Depends, HTTPException, Query
from ..database import get_session
from ..models import (
    Transaction, TransactionCreate, TransactionRead,
    TransactionUpdate, TransactionType, Category, TokenData
)
from ..auth import get_current_user, require_admin

router = APIRouter(prefix="/api/transactions", tags=["transactions"])


@router.get("/", response_model=List[TransactionRead])
async def get_transactions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
    type: Optional[TransactionType] = None,
    category: Optional[Category] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    session: Session = Depends(get_session),
    current_user: TokenData = Depends(get_current_user)
):
    query = select(Transaction)

    conditions = []
    if type:
        conditions.append(Transaction.type == type)
    if category:
        conditions.append(Transaction.category == category)
    if start_date:
        conditions.append(Transaction.date >= start_date)
    if end_date:
        conditions.append(Transaction.date <= end_date)

    if conditions:
        query = query.where(and_(*conditions))

    query = query.offset(skip).limit(limit).order_by(Transaction.date.desc())
    transactions = session.exec(query).all()
    return transactions


@router.get("/stats/monthly")
async def get_monthly_stats(
    year: int = Query(..., ge=2020, le=2100),
    month: Optional[int] = Query(None, ge=1, le=12),
    session: Session = Depends(get_session),
    current_user: TokenData = Depends(get_current_user)
):
    if month:
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)
    else:
        start_date = datetime(year, 1, 1)
        end_date = datetime(year + 1, 1, 1)

    income_stmt = select(func.sum(Transaction.amount)).where(
        and_(
            Transaction.type == TransactionType.INCOME,
            Transaction.date >= start_date,
            Transaction.date < end_date
        )
    )
    expense_stmt = select(func.sum(Transaction.amount)).where(
        and_(
            Transaction.type == TransactionType.EXPENSE,
            Transaction.date >= start_date,
            Transaction.date < end_date
        )
    )

    total_income = session.exec(income_stmt).first() or 0
    total_expense = session.exec(expense_stmt).first() or 0

    return {
        "period": f"{year}-{month:02d}" if month else str(year),
        "total_income": float(total_income),
        "total_expense": float(total_expense),
        "net_savings": float(total_income - total_expense)
    }


@router.get("/stats/category")
async def get_category_stats(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    type: Optional[TransactionType] = None,
    session: Session = Depends(get_session),
    current_user: TokenData = Depends(get_current_user)
):
    query = select(
        Transaction.category,
        func.sum(Transaction.amount).label("total"),
        func.count(Transaction.id).label("count")
    ).group_by(Transaction.category)

    conditions = []
    if start_date:
        conditions.append(Transaction.date >= start_date)
    if end_date:
        conditions.append(Transaction.date <= end_date)
    if type:
        conditions.append(Transaction.type == type)

    if conditions:
        query = query.where(and_(*conditions))

    results = session.exec(query).all()

    return [
        {
            "category": result[0],
            "total": float(result[1]),
            "count": result[2]
        }
        for result in results
    ]


@router.get("/{transaction_id}", response_model=TransactionRead)
async def get_transaction(
    transaction_id: int,
    session: Session = Depends(get_session),
    current_user: TokenData = Depends(get_current_user)
):
    transaction = session.get(Transaction, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction


@router.post("/", response_model=TransactionRead)
async def create_transaction(
    transaction: TransactionCreate,
    session: Session = Depends(get_session),
    current_user: TokenData = Depends(require_admin)
):
    db_transaction = Transaction.model_validate(transaction)
    session.add(db_transaction)
    session.commit()
    session.refresh(db_transaction)
    return db_transaction


@router.put("/{transaction_id}", response_model=TransactionRead)
async def update_transaction(
    transaction_id: int,
    transaction_update: TransactionUpdate,
    session: Session = Depends(get_session),
    current_user: TokenData = Depends(require_admin)
):
    transaction = session.get(Transaction, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    update_data = transaction_update.model_dump(exclude_unset=True)
    if update_data:
        for key, value in update_data.items():
            setattr(transaction, key, value)
        transaction.updated_at = datetime.now()
        session.add(transaction)
        session.commit()
        session.refresh(transaction)

    return transaction


@router.delete("/{transaction_id}")
async def delete_transaction(
    transaction_id: int,
    session: Session = Depends(get_session),
    current_user: TokenData = Depends(require_admin)
):
    transaction = session.get(Transaction, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    session.delete(transaction)
    session.commit()
    return {"message": "Transaction deleted successfully"}