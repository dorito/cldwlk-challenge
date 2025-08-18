import decimal
import uuid

from pydantic import BaseModel

from data.enums import (
    CreditRequestReasonEnum,
    CreditRequestStatusEnum,
    CreditRequestTypeEnum,
)

class CreditLoanSchema(BaseModel):
    guid: uuid.UUID
    profile_guid: uuid.UUID
    requested_amount: decimal.Decimal
    income: decimal.Decimal
    requested_credit_type: CreditRequestTypeEnum
    reason: CreditRequestReasonEnum
    status: CreditRequestStatusEnum
    available_amount: decimal.Decimal | None
    available_credit_type: CreditRequestTypeEnum | None
    interest_rate: decimal.Decimal | None
    webhook_url: str

class CreditLoanCreationSchema(BaseModel):
    requested_amount: decimal.Decimal
    income: decimal.Decimal
    requested_credit_type: CreditRequestTypeEnum
    reason: CreditRequestReasonEnum
    webhook_url: str
