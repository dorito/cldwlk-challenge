import uuid

from sqlalchemy import ForeignKey, text, types
from sqlalchemy.orm import Mapped, mapped_column, relationship

from data.models.base import BaseModel


class EmotionModel(BaseModel):
    __tablename__ = "emotion"

    guid: Mapped[uuid.UUID] = mapped_column(
        types.Uuid,
        primary_key=True,
        server_default=text("gen_random_uuid()"),  # use what you have on your server
    )
    trace_guid: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("emotion_trace.guid"), nullable=False
    )
    profile_guid: Mapped[uuid.UUID] = mapped_column(types.Uuid, nullable=False)
    name: Mapped[str] = mapped_column(types.String, nullable=False)
    percent: Mapped[float] = mapped_column(types.Float, nullable=False)
    trace: Mapped["EmotionTraceModel"] = relationship(back_populates="emotions")
