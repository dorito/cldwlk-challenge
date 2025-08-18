import enum

class CreditRequestTypeEnum(enum.StrEnum):
    SHORT = "short"
    MID = "mid"
    LONG = "long"
    
class CreditRequestStatusEnum(enum.StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class CreditRequestReasonEnum(enum.StrEnum):
    DEBTS = "debts"
    GIFT = "gift"
    INVESTMENT = "investment"
    PERSONAL = "personal"
