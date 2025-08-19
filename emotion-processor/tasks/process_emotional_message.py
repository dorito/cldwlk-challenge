from app.celery import app as celery_app
from app.logger import LOGGER
from data.schemas import EmotionTraceSchema
from services import EmotionService

@celery_app.task
def process_emotional_message_task(msg):
    parsed_msg = EmotionTraceSchema.parse_obj(msg)
    service = EmotionService()
    service.save_emotional_trace(parsed_msg)

