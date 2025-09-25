from decimal import Decimal
from sqlmodel import Session, select, func, and_
from fastapi import APIRouter, Depends, HTTPException
from ..database import get_session
from ..models import (
    FundPool, FundPoolRead, Transaction,
    TransactionType, TokenData
)
from ..auth import get_current_user, require_admin
from datetime import datetime

router = APIRouter(prefix="/api/fund-pool", tags=["fund-pool"])


@router.get("/", response_model=FundPoolRead)
async def get_fund_pool(
    session: Session = Depends(get_session),
    current_user: TokenData = Depends(get_current_user)
):
    # 获取或创建资金池
    fund_pool = session.exec(select(FundPool)).first()
    if not fund_pool:
        # 初始化资金池
        fund_pool = FundPool(
            initial_amount=Decimal("47830.00"),
            current_balance=Decimal("47830.00")
        )
        session.add(fund_pool)
        session.commit()
        session.refresh(fund_pool)

    # 计算总支出
    expenses_stmt = select(func.sum(Transaction.amount)).where(
        Transaction.type == TransactionType.EXPENSE
    )
    total_expenses = session.exec(expenses_stmt).first() or Decimal("0")

    # 计算总收入（包括工资、奖金等）
    income_stmt = select(func.sum(Transaction.amount)).where(
        Transaction.type == TransactionType.INCOME
    )
    total_income = session.exec(income_stmt).first() or Decimal("0")

    # 计算当前余额：初始金额 + 收入 - 支出
    current_balance = (
        fund_pool.initial_amount +
        total_income -
        total_expenses
    )

    # 更新资金池余额
    fund_pool.current_balance = current_balance
    fund_pool.last_updated = datetime.now()
    session.add(fund_pool)
    session.commit()

    return FundPoolRead(
        id=fund_pool.id,
        initial_amount=fund_pool.initial_amount,
        current_balance=current_balance,
        total_deposits=Decimal("0"),  # 不再单独计算存款
        total_expenses=total_expenses,
        total_income=total_income,
        last_updated=fund_pool.last_updated
    )


from pydantic import BaseModel

class FundPoolReset(BaseModel):
    initial_amount: Decimal

@router.put("/reset")
async def reset_fund_pool(
    data: FundPoolReset,
    session: Session = Depends(get_session),
    current_user: TokenData = Depends(require_admin)
):
    """重置资金池初始金额（仅管理员）"""
    fund_pool = session.exec(select(FundPool)).first()
    if not fund_pool:
        fund_pool = FundPool(
            initial_amount=data.initial_amount,
            current_balance=data.initial_amount
        )
    else:
        fund_pool.initial_amount = data.initial_amount
        fund_pool.last_updated = datetime.now()

    session.add(fund_pool)
    session.commit()

    return {"message": "Fund pool reset successfully", "initial_amount": data.initial_amount}