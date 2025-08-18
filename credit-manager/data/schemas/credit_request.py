import decimal
import uuid

from pydantic import BaseModel, ConfigDict

from data.enums import (
    CreditRequestReasonEnum,
    CreditRequestStatusEnum,
    CreditRequestTypeEnum,
)


class CreditResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    guid: uuid.UUID | None
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


class CreditRequestCreationSchema(BaseModel):
    idempotency_guid: uuid.UUID
    profile_guid: uuid.UUID
    requested_amount: decimal.Decimal
    income: decimal.Decimal
    requested_credit_type: CreditRequestTypeEnum
    reason: CreditRequestReasonEnum
    webhook_url: str
