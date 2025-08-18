import datetime
import uuid

from data.schemas.emotion import EmotionSchema
from pydantic import BaseModel


class EmotionTraceSchema(BaseModel):
    profile_guid: uuid.UUID
    emotions: list[EmotionSchema]
    received_at: datetime.datetime
    idempotency_guid: uuid.UUID
