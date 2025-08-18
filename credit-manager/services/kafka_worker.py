from kafka import KafkaConsumer

from app.config import Config
from app.logger import LOGGER
from services import FinancialTransactionService


class KafkaWorkerService:
    def __init__(self):
        self._financial_transaction_service = FinancialTransactionService()

    def handle(self):
        LOGGER.info("Initializing consumer..")

        consumer = KafkaConsumer(
            Config.KAFKA_FINANCIAL_TRANSACTION_TOPIC,
            group_id=Config.KAFKA_GROUP_ID,
            bootstrap_servers=Config.KAFKA_BOOTSTRAP_SERVERS,
        )

        LOGGER.info("Waiting for messages..")

        for msg in consumer:
            try:
                self._financial_transaction_service.async_process_message(msg)
            except Exception as e:
                LOGGER.error(f"Uncatched exception: {e}")
                raise e
