import uuid

from pydantic import BaseModel


class UserMetadataSchema(BaseModel):
    guid: uuid.UUID
    user_guid: uuid.UUID
    key: str
    value: str
