import uuid
from typing import Annotated, Union

from fastapi import Depends, FastAPI, Query, Response, status
from sqlalchemy.orm import Session

from app.database import ENGINE
from data.schemas import (
    CreditRequestCreationSchema,
    CreditRequestGetDataQueryParamsSchema,
    CreditResponseSchema,
    FinancialTransactionGetDataQueryParamsSchema,
    FinancialTransactionSchema,
)
from services import (
    CreditRequestService,
    FinancialTransactionService,
    HealthCheckService,
)

app = FastAPI()


def get_db_session():
    with Session(ENGINE) as DbSession:
        yield DbSession


DbSessionDep = Annotated[Session, Depends(get_db_session)]


@app.get("/internal/financial-transaction/by-profile-guid/{profile_guid}")
def get_financial_transaction_data(
    profile_guid: uuid.UUID,
    response: Response,
    db_session: DbSessionDep,
    query: Union[
        Annotated[FinancialTransactionGetDataQueryParamsSchema, Query()], None
    ] = FinancialTransactionGetDataQueryParamsSchema.parse_obj({}),
) -> list[FinancialTransactionSchema]:
    service = FinancialTransactionService(DbSession=db_session)
    financial_transaction_data = service.get_financial_transaction_history(
        profile_guid=profile_guid, limit=query.limit
    )
    if not financial_transaction_data:
        response.status_code = status.HTTP_404_NOT_FOUND
        return []
    return financial_transaction_data


@app.get("/internal/credit-request/by-profile-guid/{profile_guid}")
def get_credit_request_data(
    profile_guid: uuid.UUID,
    response: Response,
    db_session: DbSessionDep,
    query: Union[
        Annotated[CreditRequestGetDataQueryParamsSchema, Query()], None
    ] = CreditRequestGetDataQueryParamsSchema.parse_obj({}),
) -> list[CreditResponseSchema]:
    service = CreditRequestService(DbSession=db_session)
    credit_request_data = service.get_credit_request_history(
        profile_guid=profile_guid, limit=query.limit
    )
    if not credit_request_data:
        response.status_code = status.HTTP_404_NOT_FOUND
        return []
    return credit_request_data


@app.post("/internal/credit-request")
def create_credit_request(
    credit_request: CreditRequestCreationSchema,
    db_session: DbSessionDep,
    status_code=status.HTTP_201_CREATED,
) -> CreditResponseSchema:
    service = CreditRequestService(DbSession=db_session)
    created_request = service.create_credit_request(request=credit_request)
    return created_request


@app.get("/internal/health")
def health_check(response: Response):
    service = HealthCheckService()
    is_queue_healthy = service.check_queue_health()
    is_kafka_healthy = service.check_kafka_health()
    is_api_healthy = service.check_api_health()
    response.status_code = (
        status.HTTP_200_OK
        if all([is_queue_healthy, is_kafka_healthy, is_api_healthy])
        else status.HTTP_503_SERVICE_UNAVAILABLE
    )
    return {
        "celery": is_queue_healthy,
        "kafka": is_kafka_healthy,
        "api": is_api_healthy,
    }
