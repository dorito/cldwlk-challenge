import random

from app.celery import app as celery_app
from app.database import SESSION
from app.logger import LOGGER
from data.enums import CreditRequestStatusEnum
from data.models import CreditRequestModel
from services import (
    CreditAnalysisService,
    CreditRequestService,
    FinancialTransactionService,
)


@celery_app.task
def process_credit_request_task(credit_request_guid: str):
    service = CreditRequestService(SESSION)
    credit_request = service.get_by_guid(credit_request_guid)
    if credit_request is None:
        LOGGER.error(f"Credit request with guid {credit_request_guid} not found")
        return
    if credit_request.status != CreditRequestStatusEnum.PENDING.value:
        LOGGER.error(f"Credit request with guid {credit_request_guid} is not pending")
        return
    _update_credit_request(credit_request)


def _get_emotional_score(profile_guid: str):
    # TODO: make a real call to the ML model
    return round(random.uniform(0.1, 1.0), 10)


def _get_transaction_history(profile_guid: str):
    service = FinancialTransactionService(SESSION)
    transactions = service.get_financial_transaction_history(profile_guid, limit=10)
    return transactions


def _get_approved_values(profile_guid: str, credit_request: CreditRequestModel):
    service = CreditAnalysisService(SESSION)
    emotional_score = _get_emotional_score(profile_guid)
    transaction_history = _get_transaction_history(profile_guid)
    approved_values = service.get_credit_request_approved_values(
        emotional_score=emotional_score,
        requested_amount=credit_request.requested_amount,
        last_financial_transactions=transaction_history,
    )
    return approved_values


def _update_credit_request(credit_request: CreditRequestModel):
    service = CreditRequestService(SESSION)
    approved_values = _get_approved_values(credit_request.profile_guid, credit_request)
    service.update_to_approved_values(credit_request.guid, approved_values)
