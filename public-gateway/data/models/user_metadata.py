import uuid

from sqlalchemy import ForeignKey, text, types
from sqlalchemy.orm import Mapped, mapped_column, relationship

from data.models.base import BaseModel


class UserMetadataModel(BaseModel):
    __tablename__ = "user_metadata"

    guid: Mapped[uuid.UUID] = mapped_column(
        types.Uuid,
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    user_guid: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user.guid"), nullable=False, index=True
    )
    key: Mapped[str] = mapped_column(types.String, nullable=False)
    value: Mapped[str] = mapped_column(types.String, nullable=False)
    user: Mapped["UserModel"] = relationship(back_populates="user_metadata")
