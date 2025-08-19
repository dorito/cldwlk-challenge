import uuid
from typing import Annotated, Union

from fastapi import Depends, FastAPI, Query, Response, status
from sqlalchemy.orm import Session

from app.database import ENGINE
from data.schemas import EmotionTraceGetDataQueryParamsSchema, EmotionTraceSchema
from services import EmotionService, HealthCheckService

app = FastAPI()


def get_db_session():
    with Session(ENGINE) as session:
        yield session


DbSessionDep = Annotated[Session, Depends(get_db_session)]


@app.get("/internal/emotion-trace-data/by-profile-guid/{profile_guid}")
def get_emotion_trace_data(
    profile_guid: uuid.UUID,
    response: Response,
    db_session: DbSessionDep,
    query: Union[
        Annotated[EmotionTraceGetDataQueryParamsSchema, Query()], None
    ] = EmotionTraceGetDataQueryParamsSchema.parse_obj({}),
    status_code=status.HTTP_200_OK,
) -> list[EmotionTraceSchema]:
    service = EmotionService()
    emotion_trace_data = service.get_emotion_trace_data(
        session=db_session, profile_guid=profile_guid, limit=query.limit
    )
    if not emotion_trace_data:
        response.status_code = status.HTTP_404_NOT_FOUND
        return []
    return emotion_trace_data


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
