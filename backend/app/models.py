from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"


class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"


class Category(str, Enum):
    FOOD = "food"
    TRANSPORT = "transport"
    SHOPPING = "shopping"
    UTILITIES = "utilities"
    ENTERTAINMENT = "entertainment"
    MEDICAL = "medical"
    EDUCATION = "education"
    SALARY = "salary"
    BONUS = "bonus"
    OTHER = "other"


class TransactionBase(SQLModel):
    date: datetime = Field(default_factory=datetime.now)
    amount: Decimal = Field(decimal_places=2)
    type: TransactionType
    category: Category
    description: Optional[str] = Field(default=None, max_length=200)


class Transaction(TransactionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(SQLModel):
    date: Optional[datetime] = None
    amount: Optional[Decimal] = None
    type: Optional[TransactionType] = None
    category: Optional[Category] = None
    description: Optional[str] = None


class TransactionRead(TransactionBase):
    id: int
    created_at: datetime
    updated_at: datetime


class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(SQLModel):
    username: str
    role: UserRole


class FundPool(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    initial_amount: Decimal = Field(decimal_places=2, default=47830.00)
    current_balance: Decimal = Field(decimal_places=2)
    last_updated: datetime = Field(default_factory=datetime.now)


class FundPoolRead(SQLModel):
    id: int
    initial_amount: Decimal
    current_balance: Decimal
    total_deposits: Decimal
    total_expenses: Decimal
    total_income: Decimal
    last_updated: datetime