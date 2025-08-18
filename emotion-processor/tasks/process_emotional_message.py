from app.celery import app as celery_app
from app.database import SESSION
from schemas import KafkaNewEmotionMessage
from app.circuit_breakers import db_processing_breaker
from models import Emotion, EmotionTrace
from app.logger import LOGGER

@celery_app.task
def process_emotional_message(msg):
    LOGGER.info(msg)
    parsed_msg = KafkaNewEmotionMessage.parse_obj(msg)
    _save_emotional_message_into_db(parsed_msg)

@db_processing_breaker
def _save_emotional_message_into_db(msg):
    trace = SESSION.query(EmotionTrace).filter_by(idempotency_id=msg.idempotency_id).first()
    
    if trace is not None and trace.processed is True:
        LOGGER.info("Trace with idempotency id {msg.idempotency_id} is already processed, skipping")
        return
    
    if trace is None:
        trace = EmotionTrace(
            idempotency_id=msg.idempotency_id,
            profile_id=msg.profile_id,
            received_at=msg.datetime
        )
        SESSION.add(trace)
        SESSION.commit()
    else:
        SESSION.query(Emotion).filter_by(trace_guid=trace.guid).delete()
        SESSION.commit()
    
    for emotion in msg.emotions:
        emotion_record = Emotion(
            trace_guid=trace.guid,
            profile_id=msg.profile_id,
            name=emotion.name.value,
            percent=emotion.percent
        )
        SESSION.add(emotion_record)
    SESSION.commit()
    trace.processed = True
    SESSION.commit()
    LOGGER.info("Trace with idempotency id {msg.idempotency_id} succesfully processed")
