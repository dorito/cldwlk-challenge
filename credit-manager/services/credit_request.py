import decimal
import time

import requests
from sqlalchemy.orm import Session

from app.logger import LOGGER
from data.enums import CreditRequestStatusEnum
from data.models import CreditRequestModel
from data.schemas import CreditRequestCreationSchema, CreditResponseSchema


class CreditRequestService:
    def __init__(self, DbSession: Session):
        self._session = DbSession

    def get_credit_request_history(
        self, profile_guid: str, limit: int
    ) -> list[CreditRequestModel]:
        credit_requests = (
            self._session.query(CreditRequestModel)
            .filter_by(profile_guid=profile_guid)
            .order_by(CreditRequestModel.created_at.desc())
            .limit(limit)
            .all()
        )
        return credit_requests

    def get_by_guid(self, credit_request_guid: str) -> CreditRequestModel | None:
        LOGGER.info(f"Getting credit request by guid: {credit_request_guid}")
        return (
            self._session.query(CreditRequestModel)
            .filter_by(guid=credit_request_guid)
            .first()
        )

    def get_by_idempotency_guid(
        self, idempotency_guid: str
    ) -> CreditRequestModel | None:
        return (
            self._session.query(CreditRequestModel)
            .filter_by(idempotency_guid=idempotency_guid)
            .first()
        )

    def create_credit_request(
        self, request: CreditRequestCreationSchema
    ) -> CreditRequestModel:
        try:
            credit_request = self.get_by_idempotency_guid(request.idempotency_guid)
            if credit_request is not None:
                LOGGER.warning(
                    f"Credit request with idempotency guid {request.idempotency_guid} already exists"
                )
                return credit_request
            credit_request = CreditRequestModel(
                idempotency_guid=request.idempotency_guid,
                profile_guid=request.profile_guid,
                requested_amount=request.requested_amount,
                income=request.income,
                requested_credit_type=request.requested_credit_type.value,
                reason=request.reason.value,
                status=CreditRequestStatusEnum.PENDING.value,
                webhook_url=request.webhook_url,
            )
            self._session.add(credit_request)
            self._session.commit()
            self._credit_request_created_event(credit_request.guid)
            return credit_request
        except Exception as e:
            LOGGER.error(f"Error at create_credit_request: {e}")
            self._session.rollback()
            raise e

    def _credit_request_created_event(self, credit_request_guid: str):
        from tasks import process_credit_request_task

        process_credit_request_task.apply_async([credit_request_guid])

    def _credit_request_updated_event(self, credit_request_guid: str):
        from tasks import notify_credit_request_task

        notify_credit_request_task.apply_async([credit_request_guid])

    def update_to_approved_values(
        self, credit_request_guid: str, approved_values: dict
    ):
        try:
            credit_request = self.get_by_guid(credit_request_guid)
            if credit_request is None:
                LOGGER.error(
                    f"Credit request with guid {credit_request_guid} not found"
                )
                return
            credit_request.status = approved_values["status"].value
            credit_request.interest_rate = (
                approved_values["interest_rate"]
                if credit_request.status == CreditRequestStatusEnum.APPROVED.value
                else None
            )
            credit_request.available_amount = (
                approved_values["available_amount"]
                if credit_request.status == CreditRequestStatusEnum.APPROVED.value
                else None
            )
            credit_request.available_credit_type = (
                approved_values["credit_type"].value
                if credit_request.status == CreditRequestStatusEnum.APPROVED.value
                else None
            )
            self._session.commit()
            self._credit_request_updated_event(credit_request.guid)
        except Exception as e:
            LOGGER.error(f"Error at update_status_and_interest_rate: {e}")
            self._session.rollback()
            raise e

    def notify_webhook(self, credit_request: CreditRequestModel):
        self._session.refresh(credit_request)
        webhook_url = credit_request.webhook_url
        payload = CreditResponseSchema.from_orm(credit_request).model_dump(mode="json")
        try:
            response = requests.post(webhook_url, json=payload)
            response.raise_for_status()
        except requests.RequestException as e:
            LOGGER.error(f"Error notifying webhook: url {webhook_url} | error {e}")
