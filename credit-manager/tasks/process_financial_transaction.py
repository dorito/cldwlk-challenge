from app.celery import app as celery_app
from app.circuit_breakers import db_processing_breaker
from app.database import DbSession
from app.logger import LOGGER
from data.models import FinancialTransactionModel
from data.schemas import FinancialTransactionCreationSchema


@celery_app.task
def process_financial_transaction_task(msg):
    parsed_msg = FinancialTransactionCreationSchema.parse_obj(msg)
    _save_financial_transaction_into_db(parsed_msg)


@db_processing_breaker
def _save_financial_transaction_into_db(msg):
    transaction = (
        DbSession.query(FinancialTransactionModel)
        .filter_by(idempotency_guid=msg.idempotency_guid)
        .first()
    )

    if transaction is not None:
        LOGGER.info(
            "Transaction with idempotency id {msg.idempotency_guid} is already processed, skipping"
        )
        return

    transaction = FinancialTransactionModel(
        idempotency_guid=msg.idempotency_guid,
        profile_guid=msg.profile_guid,
        received_at=msg.datetime,
        source=msg.source,
        reason=msg.reason,
        amount=msg.amount,
        is_paid=msg.is_paid,
        paid_at=msg.paid_at,
        due_at=msg.due_at,
    )
    DbSession.add(transaction)
    DbSession.commit()
    LOGGER.info(
        "Transaction with idempotency id {msg.idempotency_guid} succesfully processed"
    )
