from pydantic import BaseModel

from data.enums import EmotionEnum


class EmotionSchema(BaseModel):
    name: EmotionEnum
    percent: float
