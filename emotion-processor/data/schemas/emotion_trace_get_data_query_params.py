from pydantic import BaseModel


class EmotionTraceGetDataQueryParamsSchema(BaseModel):
    limit: int = 100
