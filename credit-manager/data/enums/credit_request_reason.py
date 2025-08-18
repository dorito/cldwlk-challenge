import enum


class CreditRequestReasonEnum(enum.Enum):
    DEBTS = "debts"
    GIFT = "gift"
    INVESTMENT = "investment"
    PERSONAL = "personal"
