from app.config import Config
from app.logger import LOGGER
from kafka import KafkaConsumer
from services import EmotionService


class KafkaWorkerService:
    def __init__(self):
        self._emotion_service = EmotionService()

    def handle(self):
        LOGGER.info("Initializing consumer..")

        consumer = KafkaConsumer(
            Config.KAFKA_EMOTIONAL_TOPIC_NAME,
            group_id=Config.KAFKA_GROUP_ID,
            bootstrap_servers=Config.KAFKA_BOOTSTRAP_SERVERS,
        )

        LOGGER.info("Waiting for messages..")

        for msg in consumer:
            try:
                self._emotion_service.async_process_message(msg)
            except Exception as e:
                LOGGER.error(f"Uncatched exception: {e}")
                raise e
