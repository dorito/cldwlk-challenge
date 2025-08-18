import datetime
import uuid

from pydantic import BaseModel

from data.schemas.emotion import EmotionSchema


class EmotionTraceSchema(BaseModel):
    profile_id: uuid.UUID
    emotions: list[EmotionSchema]
    received_at: datetime.datetime
    idempotency_id: uuid.UUID
