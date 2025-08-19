import enum


class FinancialTransactionSourceEnum(enum.StrEnum):
    INTERNAL = "internal"
    EXTERNAL = "external"


class FinancialTransactionReasonEnum(enum.StrEnum):
    DEBTS = "debts"
    GIFT = "gift"
    INVESTMENT = "investment"
    OTHER = "other"
