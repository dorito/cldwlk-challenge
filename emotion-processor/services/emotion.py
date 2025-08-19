import time

from pydantic import ValidationError
from typing import Optional
from app.logger import LOGGER
from data.models import EmotionTraceModel, EmotionModel
from data.schemas import EmotionTraceSchema
from sqlalchemy.orm import Session

class EmotionService:
    def __init__(self, db_session: Optional[Session] = None):
        self._session = db_session
        
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
        except Exception as e:
            LOGGER.error(f"Error processing message {message.value}: {e}")
            raise e

    def _async_process_message(self, message):
        from tasks import process_emotional_message_task
        process_emotional_message_task.apply_async([message])

    def save_emotional_trace(self, msg):
        trace = (
            self._session.query(EmotionTraceModel)
            .filter_by(idempotency_guid=msg.idempotency_guid)
            .first()
        )

        if trace is not None and trace.processed is True:
            LOGGER.warning(
                "Trace with idempotency guid {msg.idempotency_guid} is already processed, skipping"
            )
            return

        if trace is None:
            trace = EmotionTraceModel(
                idempotency_guid=msg.idempotency_guid,
                profile_guid=msg.profile_guid,
                received_at=msg.received_at,
            )
            self._session.add(trace)
            self._session.commit()
        else:
            self._session.query(EmotionModel).filter_by(trace_guid=trace.guid).delete()
            self._session.commit()

        for emotion in msg.emotions:
            emotion_record = EmotionModel(
                trace_guid=trace.guid,
                profile_guid=msg.profile_guid,
                name=emotion.name.value,
                percent=emotion.percent,
            )
            self._session.add(emotion_record)
        self._session.commit()
        trace.processed = True
        self._session.commit()
        LOGGER.info(
            "Trace with idempotency id {msg.idempotency_guid} succesfully processed"
        )
