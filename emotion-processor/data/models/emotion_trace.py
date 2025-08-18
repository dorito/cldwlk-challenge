import datetime
import uuid

from sqlalchemy import text, types
from sqlalchemy.orm import Mapped, mapped_column, relationship

from data.models.base import BaseModel


class EmotionTraceModel(BaseModel):
    __tablename__ = "emotion_trace"

    guid: Mapped[uuid.UUID] = mapped_column(
        types.Uuid, primary_key=True, server_default=text("gen_random_uuid()")
    )
    idempotency_id: Mapped[uuid.UUID] = mapped_column(types.Uuid, nullable=False)
    profile_id: Mapped[uuid.UUID] = mapped_column(types.Uuid, nullable=False)
    received_at: Mapped[datetime.datetime] = mapped_column(
        types.DateTime, nullable=False
    )
    processed: Mapped[bool] = mapped_column(types.Boolean, default=False)
    emotions: Mapped[list["Emotion"]] = relationship(back_populates="trace")
