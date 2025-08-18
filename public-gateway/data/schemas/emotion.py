from data.enums import EmotionEnum

from pydantic import BaseModel
import uuid
import datetime

class EmotionSchema(BaseModel):
    name: EmotionEnum
    percent: float

class EmotionTraceCreationSchema(BaseModel):
    emotions: list[EmotionSchema]

class EmotionTraceSchema(BaseModel):
    emotions: list[EmotionSchema]
    received_at: datetime.datetime