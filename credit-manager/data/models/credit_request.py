import datetime
import decimal
import uuid

from sqlalchemy import text, types
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from data.models.base import BaseModel


class CreditRequestModel(BaseModel):
    __tablename__ = "credit_request"

    guid: Mapped[uuid.UUID] = mapped_column(
        types.Uuid, primary_key=True, server_default=text("gen_random_uuid()")
    )
    idempotency_guid: Mapped[uuid.UUID] = mapped_column(types.Uuid, nullable=False)
    profile_guid: Mapped[uuid.UUID] = mapped_column(types.Uuid, nullable=False)
    requested_amount: Mapped[decimal.Decimal] = mapped_column(
        types.DECIMAL(precision=14, scale=2), nullable=False
    )
    income: Mapped[decimal.Decimal] = mapped_column(
        types.DECIMAL(precision=14, scale=2), nullable=False
    )
    requested_credit_type: Mapped[str] = mapped_column(
        types.String(255), nullable=False
    )
    reason: Mapped[str] = mapped_column(types.String(255), nullable=False)
    status: Mapped[str] = mapped_column(types.String(255), nullable=False)
    available_amount: Mapped[decimal.Decimal] = mapped_column(
        types.DECIMAL(precision=14, scale=2), nullable=True
    )
    available_credit_type: Mapped[str] = mapped_column(types.String(255), nullable=True)
    interest_rate: Mapped[decimal.Decimal] = mapped_column(
        types.DECIMAL(precision=8, scale=2), nullable=True
    )
    webhook_url: Mapped[str] = mapped_column(types.String(255), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        types.DateTime, nullable=False, server_default=func.now()
    )
