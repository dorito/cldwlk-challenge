from app.celery import app as celery_app
from app.database import SESSION
from app.logger import LOGGER
from data.enums import CreditRequestStatusEnum
from services.credit_request import CreditRequestService


@celery_app.task
def notify_credit_request_task(credit_request_guid: str):
    service = CreditRequestService(SESSION)
    credit_request = service.get_by_guid(credit_request_guid)
    if credit_request is None:
        LOGGER.error(f"Credit request with guid {credit_request_guid} not found")
        return
    if credit_request.status == CreditRequestStatusEnum.PENDING:
        LOGGER.error(f"Credit request with guid {credit_request_guid} is pending")
        return
    service.notify_webhook(credit_request)
