import datetime
import uuid
from hashlib import sha256

from sqlalchemy.orm import Session

from app.logger import LOGGER
from data.models import UserMetadataModel, UserModel


class UserService:
    def __init__(self, db_session: Session):
        self._session = db_session

    def get_user_by_email(self, email: str) -> UserModel | None:
        user = self._session.query(UserModel).filter_by(email=email).first()
        return user

    def create_user(self, email: str, password: str) -> UserModel | None:
        try:
            if self.get_user_by_email(email):
                raise Exception("User already exists")
            user = UserModel(
                email=email,
                hashed_password=sha256(password.encode()).hexdigest(),
                api_key=str(uuid.uuid4()),
                registered_on=datetime.datetime.now(),
            )
            self._session.add(user)
            self._session.commit()
            user_metadata = UserMetadataModel(
                user_guid=user.guid, key="profile_guid", value=str(uuid.uuid4())
            )
            self._session.add(user_metadata)
            self._session.commit()
            self._session.refresh(user)
            return user
        except Exception as e:
            LOGGER.error(f"Failed to create user: {e}")
            self._session.rollback()
            return None

    def fetch_user_api_key(self, email: str, password: str) -> UserModel | None:
        user = self.get_user_by_email(email)
        if user and user.hashed_password == sha256(password.encode()).hexdigest():
            return user
        return None

    def get_user_by_api_key(self, api_key: str) -> UserModel | None:
        user = self._session.query(UserModel).filter_by(api_key=api_key).first()
        return user

    def get_metadata_for_user(self, user: UserModel, metadata_key: str) -> str | None:
        metadata = (
            self._session.query(UserMetadataModel)
            .filter_by(user_guid=user.guid, key=metadata_key)
            .first()
        )
        return metadata.value if metadata else None
