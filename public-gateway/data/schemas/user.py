import datetime
import uuid

from pydantic import BaseModel, EmailStr

from data.schemas.user_metadata_schema import UserMetadataSchema


class UserSchema(BaseModel):
    guid: uuid.UUID
    email: EmailStr
    api_key: str
    user_metadata: list[UserMetadataSchema] | None
    registered_on: datetime.datetime


class UserCreationSchema(BaseModel):
    email: EmailStr
    password: str


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str
