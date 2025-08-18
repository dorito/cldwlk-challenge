from sqlalchemy.orm import Session
from kafka import KafkaProducer

from data.models import UserModel
from app.logger import LOGGER
from data.schemas import EmotionTraceCreationSchema, EmotionTraceSchema
from services import UserService
from app.config import Config
import json
import uuid
import datetime
import requests

class EmotionService:
  def __init__(self, db_session: Session, user: UserModel):
      self._session = db_session
      self._user = user
      self._kafka_producer = KafkaProducer(bootstrap_servers=Config.KAFKA_BOOTSTRAP_SERVERS)
      self._user_service = UserService(db_session)
      
  def create_emotion(self, emotion_data: EmotionTraceCreationSchema) -> EmotionTraceSchema:
      try:
          profile_guid = self._user_service.get_metadata_for_user(self._user, "profile_guid")
          if not profile_guid:
              raise Exception("Profile GUID not found")
          emotion_data_as_dict = emotion_data.dict()
          emotion_data_as_dict['idempotency_guid'] = str(uuid.uuid4())
          emotion_data_as_dict['profile_guid'] = profile_guid
          emotion_data_as_dict['received_at'] = datetime.datetime.now().isoformat()
          data_as_byte = f"{json.dumps(emotion_data_as_dict)}".encode("utf-8")
          self._kafka_producer.send(Config.KAFKA_EMOTIONAL_TOPIC_NAME, data_as_byte)
          return EmotionTraceSchema(**emotion_data_as_dict)
      except Exception as e:
          LOGGER.error(f"Error creating emotion: {e}")
          raise e

  def list_emotions(self) -> list[EmotionTraceSchema]:
        try:
          profile_guid = self._user_service.get_metadata_for_user(self._user, "profile_guid")
          if not profile_guid:
              raise Exception("Profile GUID not found")
          response = requests.get(f"{Config.EMOTION_PROCESSOR_LIST_TRACE_ENDPOINT}{profile_guid}")
          response.raise_for_status()
          emotions = [EmotionTraceSchema(**emotion) for emotion in response.json()]
          return emotions
        except Exception as e:
          if e.response.status_code == 404:
              return []
          LOGGER.error(f"Error listing emotions: {e}")
          raise e