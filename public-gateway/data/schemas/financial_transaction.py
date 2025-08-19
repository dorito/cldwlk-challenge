import datetime
import decimal
import uuid

from pydantic import BaseModel

from data.enums import FinancialTransactionReasonEnum, FinancialTransactionSourceEnum


class FinancialTransactionSchema(BaseModel):
    source: FinancialTransactionSourceEnum
    reason: FinancialTransactionReasonEnum
    amount: decimal.Decimal
    is_paid: bool
    paid_at: datetime.datetime | None
    due_at: datetime.datetime
    # received_at: datetime.datetime


class FinancialTransactionCreationSchema(FinancialTransactionSchema): ...
