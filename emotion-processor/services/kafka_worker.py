from kafka import KafkaConsumer
from app.logger import LOGGER
from app.config import Config
from schemas import KafkaNewEmotionMessage
from pydantic import ValidationError
from pybreaker import CircuitBreakerError
from tasks import process_emotional_message
import time
from app.circuit_breakers import kafka_processing_breaker

class KafkaWorkerService:
    def handle(self):
        consumer = KafkaConsumer(
            Config.KAFKA_EMOTIONAL_TOPIC_NAME,
            group_id=Config.KAFKA_GROUP_ID,
            bootstrap_servers=Config.KAFKA_BOOTSTRAP_SERVERS
        )
        
        LOGGER.info("Waiting for messages..")
        
        for msg in consumer:
          try:
            parsed_msg = KafkaNewEmotionMessage.model_validate_json(msg.value)
            self._async_process_message(parsed_msg.model_dump(mode='json'))
            LOGGER.debug(f"Processed message: {parsed_msg}")
          except ValidationError as e:
            LOGGER.error(f"Validation error for {msg.value}: {e}")
            continue
          except CircuitBreakerError:
            timeout = kafka_processing_breaker.reset_timeout
            LOGGER.error(f"Circuit breaker error occurred when executing kafka worker, retrying after {timeout} seconds")
            time.sleep(timeout)
            # TODO: put the failed message in a DLQ to be reprocessed
            continue
    
    @kafka_processing_breaker
    def _async_process_message(self, message):
        process_emotional_message.apply_async([message])
