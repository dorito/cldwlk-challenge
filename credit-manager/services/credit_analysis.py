import datetime
import decimal
import time

from sqlalchemy.orm import Session

from app.logger import LOGGER
from data.enums import CreditRequestStatusEnum, CreditRequestTypeEnum
from data.models import FinancialTransactionModel


class CreditAnalysisService:
    def __init__(self, DbSession: Session):
        self._session = DbSession

    def get_credit_request_approved_values(
        self,
        emotional_score: float,
        requested_amount: float,
        last_financial_transactions: list[FinancialTransactionModel],
    ):
        chance_of_payment = self._calculate_chance_of_payment(
            emotional_score, requested_amount, last_financial_transactions
        )
        (
            credit_type,
            available_amount,
        ) = self._get_credit_request_tier_and_available_amount(
            chance_of_payment, float(requested_amount)
        )
        status, interest_rate = self._get_credit_request_status_and_interest_rate(
            chance_of_payment
        )
        return {
            "credit_type": credit_type
            if status != CreditRequestStatusEnum.REJECTED.value
            else None,
            "available_amount": available_amount
            if status != CreditRequestStatusEnum.REJECTED.value
            else None,
            "status": status,
            "interest_rate": interest_rate,
        }

    def _get_credit_request_tier_and_available_amount(
        self,
        chance_of_payment_rate: float,
        requested_amount: float,
    ):
        available_amount = 0
        credit_type = None

        # TODO: make something better than a tier system
        if chance_of_payment_rate <= 1 and chance_of_payment_rate > 0.9:
            available_amount = requested_amount
        elif chance_of_payment_rate <= 0.9 and chance_of_payment_rate > 0.75:
            available_amount = requested_amount * 0.9
        elif chance_of_payment_rate <= 0.75 and chance_of_payment_rate > 0.5:
            available_amount = requested_amount * 0.5
        elif chance_of_payment_rate <= 0.5 and chance_of_payment_rate > 0.35:
            available_amount = requested_amount * 0.3
        else:
            available_amount = requested_amount * 0.1

        if available_amount >= 100000:
            credit_type = CreditRequestTypeEnum.LONG
        elif available_amount >= 20000 and available_amount < 100000:
            credit_type = CreditRequestTypeEnum.MEDIUM
        else:
            credit_type = CreditRequestTypeEnum.SHORT
        return credit_type, decimal.Decimal(available_amount)

    def _get_credit_request_status_and_interest_rate(
        self, chance_of_payment_rate: float
    ):
        status = None
        interest_rate = decimal.Decimal("0")

        # TODO: make something better than a tier system
        if chance_of_payment_rate <= 1 and chance_of_payment_rate > 0.9:
            status = CreditRequestStatusEnum.APPROVED
            interest_rate = 3
        elif chance_of_payment_rate <= 0.9 and chance_of_payment_rate > 0.75:
            status = CreditRequestStatusEnum.APPROVED
            interest_rate = 5
        elif chance_of_payment_rate <= 0.75 and chance_of_payment_rate > 0.5:
            status = CreditRequestStatusEnum.APPROVED
            interest_rate = 10
        elif chance_of_payment_rate <= 0.5 and chance_of_payment_rate > 0.35:
            status = CreditRequestStatusEnum.APPROVED
            interest_rate = 35
        else:
            status = CreditRequestStatusEnum.REJECTED
        return status, decimal.Decimal(interest_rate)

    def _calculate_chance_of_payment(
        self,
        emotional_score: float,
        requested_amount: float,
        last_financial_transactions: list[FinancialTransactionModel],
    ):
        risk = 0
        base_time = datetime.datetime.now()
        financial_weight = 0.25

        # first we get all the transaction values separated by type
        pending_amount = sum(
            txn.amount
            for txn in last_financial_transactions
            if txn.is_paid is False and txn.due_at > base_time
        )
        paid_amount = sum(
            txn.amount
            for txn in last_financial_transactions
            if txn.is_paid is True and txn.due_at <= base_time
        )
        paid_in_advance_amount = sum(
            txn.amount
            for txn in last_financial_transactions
            if txn.is_paid is True and txn.due_at > base_time
        )
        late_amount = sum(
            txn.amount
            for txn in last_financial_transactions
            if txn.is_paid is False and txn.due_at <= base_time
        )
        transactioned_amount = paid_amount + paid_in_advance_amount + late_amount

        # then we update the risk variable
        if late_amount > paid_amount:
            risk += late_amount / (late_amount + paid_amount)
        if paid_in_advance_amount > 0:
            risk -= paid_in_advance_amount / (paid_in_advance_amount + paid_amount)
        if (transactioned_amount > 0) and pending_amount >= transactioned_amount:
            risk = 1  # end user is getting credit and hasn't paid any of it yet
        if requested_amount >= (transactioned_amount * 2):
            risk = (
                1  # end user is requesting more than double their transactioned amount
            )

        # now, we normalize the risk and emotional_score values (it can't be bigger than 1 and lower than 0)
        if risk > 1:
            risk = 1
        if risk < 0:
            risk = 0

        if emotional_score > 1:
            emotional_score = 1
        if emotional_score < 0:
            emotional_score = 0

        # finally we calculate the probability of the end user paying up the solicited credit
        chance_of_payment_percent = 1 - risk
        return (emotional_score) + (chance_of_payment_percent * financial_weight)
