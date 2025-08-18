import uuid
from models.base_model import BaseModel
from sqlalchemy import text, types, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
import datetime

class Emotion(BaseModel):
    __tablename__ = "emotion"

    guid: Mapped[uuid.UUID] = mapped_column(
        types.Uuid,
        primary_key=True,
        server_default=text("gen_random_uuid()") # use what you have on your server
    )
    trace_guid: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("emotion_trace.guid"),
        nullable=False
    )
    profile_id: Mapped[uuid.UUID] = mapped_column(
        types.Uuid,
        nullable=False
    )
    name: Mapped[str] = mapped_column(
        types.String,
        nullable=False
    )
    percent: Mapped[float] = mapped_column(
        types.Float,
        nullable=False
    )
    trace: Mapped["EmotionTrace"] = relationship(back_populates="emotions")
