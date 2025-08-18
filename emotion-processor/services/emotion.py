import time

from app.circuit_breakers import celery_processing_breaker
from app.logger import LOGGER
from data.models import EmotionTraceModel
from data.schemas import EmotionTraceSchema
from pybreaker import CircuitBreakerError
from pydantic import ValidationError
from sqlalchemy.orm import Session
from tasks import process_emotional_message_task


class EmotionService:
    def get_emotion_trace_data(
        self, session: Session, profile_guid: str, limit: int
    ) -> list[EmotionTraceModel]:
        emotion_traces = (
            session.query(EmotionTraceModel)
            .filter_by(profile_guid=profile_guid)
            .order_by(EmotionTraceModel.received_at.desc())
            .limit(limit)
            .all()
        )
        return emotion_traces

    def async_process_message(self, message):
        try:
            parsed_msg = EmotionTraceSchema.model_validate_json(message.value)
            self._async_process_message(parsed_msg.model_dump(mode="json"))
            LOGGER.debug(f"Processed message: {parsed_msg}")
        except ValidationError as e:
            LOGGER.error(f"Validation error for {message.value}: {e}")
        except CircuitBreakerError:
            timeout = celery_processing_breaker.reset_timeout
            LOGGER.error(
                f"Circuit breaker error occurred when executing kafka worker, retrying after {timeout} seconds"
            )
            time.sleep(timeout)
            # TODO: put the failed message in a DLQ to be reprocessed

    @celery_processing_breaker
    def _async_process_message(self, message):
        process_emotional_message_task.apply_async([message])
