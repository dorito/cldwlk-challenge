from sqlalchemy.orm import Session

from data.models import UserModel
from app.logger import LOGGER
from data.schemas import CreditLoanCreationSchema, CreditLoanSchema
from services import UserService
from app.config import Config
import json
import uuid
import datetime
import requests

class CreditLoanService:
    def __init__(self, db_session: Session, user: UserModel):
        self._session = db_session
        self._user = user
        self._user_service = UserService(db_session)

    def create_loan(self, loan_data: CreditLoanCreationSchema) -> CreditLoanSchema:
      try:
          profile_guid = self._user_service.get_metadata_for_user(self._user, "profile_guid")
          if not profile_guid:
              raise Exception("Profile GUID not found")
          loan_data_as_dict = loan_data.dict()
          loan_data_as_dict['requested_amount'] = str(loan_data.requested_amount)
          loan_data_as_dict['income'] = str(loan_data.income)
          loan_data_as_dict['idempotency_guid'] = str(uuid.uuid4())
          loan_data_as_dict['profile_guid'] = profile_guid
          data_as_json = json.dumps(loan_data_as_dict)
          response = requests.post(Config.CREDIT_MANAGER_CREDIT_REQUEST_CREATE_ENDPOINT, data=data_as_json, headers={"Content-Type": "application/json"})
          response.raise_for_status()
          credit_request = CreditLoanSchema.parse_obj(response.json())
          return credit_request
      except Exception as e:
          LOGGER.error(f"Error creating credit loan: {e}")
          raise e

    def list_loans(self) -> list[CreditLoanSchema]:
        try:
            profile_guid = self._user_service.get_metadata_for_user(self._user, "profile_guid")
            if not profile_guid:
                raise Exception("Profile GUID not found")
            response = requests.get(f"{Config.CREDIT_MANAGER_CREDIT_REQUEST_LIST_ENDPOINT}{profile_guid}")
            response.raise_for_status()
            credit_requests = [CreditLoanSchema(**credit_request) for credit_request in response.json()]
            return credit_requests
        except Exception as e:
            LOGGER.error(f"Error listing credit loans: {e}")
            raise e
