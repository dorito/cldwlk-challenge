import time
from typing import Optional

from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.logger import LOGGER
from data.models import FinancialTransactionModel
from data.schemas import FinancialTransactionCreationSchema


class FinancialTransactionService:
    def __init__(self, DbSession: Optional[Session] = None):
        self._session = DbSession

    def get_financial_transaction_history(
        self, profile_guid: str, limit: int
    ) -> list[FinancialTransactionModel]:
        financial_transactions = (
            self._session.query(FinancialTransactionModel)
            .filter_by(profile_guid=profile_guid)
            .order_by(FinancialTransactionModel.received_at.desc())
            .limit(limit)
            .all()
        )
        return financial_transactions

    def async_process_message(self, message):
        try:
            parsed_msg = FinancialTransactionCreationSchema.model_validate_json(
                message.value
            )
            self._async_process_message(parsed_msg.model_dump(mode="json"))
            LOGGER.debug(f"Processed message: {parsed_msg}")
        except ValidationError as e:
            LOGGER.error(f"Validation error for {message.value}: {e}")
        except Exception as e:
            LOGGER.error(f"Error processing message {message.value}: {e}")
            raise e

    def _async_process_message(self, message):
        from tasks import process_financial_transaction_task

        process_financial_transaction_task.apply_async([message])
