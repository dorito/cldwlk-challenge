import datetime
import uuid

from pydantic import BaseModel

from data.enums import EmotionEnum


class EmotionSchema(BaseModel):
    name: EmotionEnum
    percent: float


class EmotionTraceCreationSchema(BaseModel):
    emotions: list[EmotionSchema]


class EmotionTraceSchema(BaseModel):
    emotions: list[EmotionSchema]
    received_at: datetime.datetime
