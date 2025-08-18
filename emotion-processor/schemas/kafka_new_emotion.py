from pydantic import BaseModel
import uuid
import datetime
from enums.emotions import EmotionEnum

class KafkaEmotion(BaseModel):
  name: EmotionEnum
  percent: float

class KafkaNewEmotionMessage(BaseModel):
  profile_id: uuid.UUID
  emotions: list[KafkaEmotion]
  datetime: datetime.datetime
  idempotency_id: uuid.UUID