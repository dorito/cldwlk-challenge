from typing import Optional
import datetime
import decimal
import uuid

from pydantic import BaseModel

from data.enums import FinancialTransactionReasonEnum, FinancialTransactionSourceEnum


class FinancialTransactionBaseSchema(BaseModel):
    profile_guid: uuid.UUID
    source: FinancialTransactionSourceEnum
    reason: FinancialTransactionReasonEnum
    amount: decimal.Decimal
    is_paid: bool
    paid_at: Optional[datetime.datetime] | None
    due_at: datetime.datetime
    received_at: datetime.datetime

class FinancialTransactionSchema(FinancialTransactionBaseSchema):
    guid: Optional[uuid.UUID] | None

class FinancialTransactionCreationSchema(FinancialTransactionBaseSchema):
    idempotency_guid: uuid.UUID
