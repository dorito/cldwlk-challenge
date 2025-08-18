import enum


class CreditRequestReasonEnum(enum.StrEnum):
    DEBTS = "debts"
    GIFT = "gift"
    INVESTMENT = "investment"
    PERSONAL = "personal"
