import datetime
import decimal
import uuid

from sqlalchemy import text, types
from sqlalchemy.orm import Mapped, mapped_column

from data.models.base import BaseModel


class FinancialTransactionModel(BaseModel):
    __tablename__ = "financial_transaction"

    guid: Mapped[uuid.UUID] = mapped_column(
        types.Uuid, primary_key=True, server_default=text("gen_random_uuid()")
    )
    idempotency_guid: Mapped[uuid.UUID] = mapped_column(types.Uuid, nullable=False, index=True)
    profile_guid: Mapped[uuid.UUID] = mapped_column(types.Uuid, nullable=False, index=True)
    source: Mapped[str] = mapped_column(types.String(255), nullable=False)
    reason: Mapped[str] = mapped_column(types.String(255), nullable=False)
    amount: Mapped[decimal.Decimal] = mapped_column(
        types.DECIMAL(precision=14, scale=2), nullable=False
    )
    is_paid: Mapped[bool] = mapped_column(types.Boolean, default=False)
    paid_at: Mapped[datetime.datetime] = mapped_column(types.DateTime, nullable=True)
    due_at: Mapped[datetime.datetime] = mapped_column(types.DateTime, nullable=False)
    received_at: Mapped[datetime.datetime] = mapped_column(
        types.DateTime, nullable=False
    )
