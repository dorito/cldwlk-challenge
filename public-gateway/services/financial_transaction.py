import datetime
import json
import uuid

import requests
from kafka import KafkaProducer
from sqlalchemy.orm import Session

from app.config import Config
from app.logger import LOGGER
from data.models import UserModel
from data.schemas import FinancialTransactionCreationSchema, FinancialTransactionSchema
from services.user import UserService


class FinancialTransactionService:
    def __init__(self, db_session: Session, user: UserModel):
        self._session = db_session
        self._user = user
        self._kafka_producer = KafkaProducer(
            bootstrap_servers=Config.KAFKA_BOOTSTRAP_SERVERS
        )
        self._user_service = UserService(db_session)

    def create_financial_transaction(
        self, transaction_data: FinancialTransactionCreationSchema
    ) -> FinancialTransactionSchema:
        try:
            profile_guid = self._user_service.get_metadata_for_user(
                self._user, "profile_guid"
            )
            if not profile_guid:
                raise Exception("Profile GUID not found")
            transaction_data_as_dict = transaction_data.dict()
            transaction_data_as_dict["amount"] = str(transaction_data.amount)
            transaction_data_as_dict["idempotency_guid"] = str(uuid.uuid4())
            transaction_data_as_dict["profile_guid"] = profile_guid
            transaction_data_as_dict["received_at"] = (
                datetime.datetime.now().isoformat()
            )
            transaction_data_as_dict["paid_at"] = (
                transaction_data.paid_at.isoformat()
                if transaction_data.paid_at
                else None
            )
            transaction_data_as_dict["due_at"] = (
                transaction_data.due_at.isoformat() if transaction_data.due_at else None
            )
            data_as_byte = f"{json.dumps(transaction_data_as_dict)}".encode("utf-8")
            self._kafka_producer.send(
                Config.KAFKA_FINANCIAL_TRANSACTION_TOPIC, data_as_byte
            )
            return FinancialTransactionSchema(**transaction_data_as_dict)
        except Exception as e:
            LOGGER.error(f"Error creating financial transaction: {e}")
            raise e

    def list_financial_transactions(self) -> list[FinancialTransactionSchema]:
        try:
            profile_guid = self._user_service.get_metadata_for_user(
                self._user, "profile_guid"
            )
            if not profile_guid:
                raise Exception("Profile GUID not found")
            response = requests.get(
                f"{Config.CREDIT_MANAGER_FINANCIAL_TRANSACTION_LIST_ENDPOINT}{profile_guid}"
            )
            response.raise_for_status()
            transactions = [
                FinancialTransactionSchema(**transaction)
                for transaction in response.json()
            ]
            return transactions
        except Exception as e:
            if e.response.status_code == 404:
                return []
            LOGGER.error(f"Error listing financial transactions: {e}")
            raise e
