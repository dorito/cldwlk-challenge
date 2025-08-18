from app.celery import app as celery_app
from app.circuit_breakers import db_processing_breaker
from app.database import DbSession
from app.logger import LOGGER
from data.models import EmotionModel, EmotionTraceModel
from data.schemas import EmotionTraceSchema


@celery_app.task
def process_emotional_message_task(msg):
    LOGGER.info(msg)
    parsed_msg = EmotionTraceSchema.parse_obj(msg)
    _save_emotional_message_into_db(parsed_msg)


@db_processing_breaker
def _save_emotional_message_into_db(msg):
    trace = (
        DbSession.query(EmotionTraceModel)
        .filter_by(idempotency_id=msg.idempotency_id)
        .first()
    )

    if trace is not None and trace.processed is True:
        LOGGER.info(
            "Trace with idempotency id {msg.idempotency_id} is already processed, skipping"
        )
        return

    if trace is None:
        trace = EmotionTraceModel(
            idempotency_id=msg.idempotency_id,
            profile_guid=msg.profile_guid,
            received_at=msg.datetime,
        )
        DbSession.add(trace)
        DbSession.commit()
    else:
        DbSession.query(EmotionModel).filter_by(trace_guid=trace.guid).delete()
        DbSession.commit()

    for emotion in msg.emotions:
        emotion_record = EmotionModel(
            trace_guid=trace.guid,
            profile_guid=msg.profile_guid,
            name=emotion.name.value,
            percent=emotion.percent,
        )
        DbSession.add(emotion_record)
    DbSession.commit()
    trace.processed = True
    DbSession.commit()
    LOGGER.info("Trace with idempotency id {msg.idempotency_id} succesfully processed")
