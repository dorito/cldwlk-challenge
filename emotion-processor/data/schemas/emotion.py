from data.enums import EmotionEnum
from pydantic import BaseModel


class EmotionSchema(BaseModel):
    name: EmotionEnum
    percent: float
