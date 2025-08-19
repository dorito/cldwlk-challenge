import datetime
import uuid

from sqlalchemy import text, types
from sqlalchemy.orm import Mapped, mapped_column, relationship

from data.models.base import BaseModel


class UserModel(BaseModel):
    __tablename__ = "user"

    guid: Mapped[uuid.UUID] = mapped_column(
        types.Uuid, primary_key=True, server_default=text("gen_random_uuid()")
    )
    email: Mapped[str] = mapped_column(types.String, nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(types.String, nullable=False)
    api_key: Mapped[str] = mapped_column(types.String, nullable=False)
    user_metadata: Mapped[list["UserMetadataModel"]] = relationship(
        back_populates="user"
    )
    registered_on: Mapped[datetime.datetime] = mapped_column(
        types.DateTime, nullable=False
    )
