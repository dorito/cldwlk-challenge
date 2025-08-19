from typing import Annotated

from fastapi import Depends, FastAPI, Request, Response, status, HTTPException
from sqlalchemy.orm import Session

from app.database import ENGINE
from app.logger import LOGGER
from data.models import UserModel
from data.schemas import (
    CreditLoanCreationSchema,
    CreditLoanSchema,
    EmotionTraceCreationSchema,
    EmotionTraceSchema,
    ErrorSchema,
    FinancialTransactionCreationSchema,
    FinancialTransactionSchema,
    UserCreationSchema,
    UserLoginSchema,
    UserSchema,
)
from services import (
    CreditLoanService,
    EmotionService,
    FinancialTransactionService,
    HealthCheckService,
    UserService,
)

app = FastAPI()


def get_db_session():
    with Session(ENGINE) as session:
        yield session


DbSessionDep = Annotated[Session, Depends(get_db_session)]


async def get_user_by_api_key(request: Request, db_session: DbSessionDep):
    service = UserService(db_session)
    api_key = request.headers.get("Authorization", "").replace("Bearer ", "")
    LOGGER.info(f"API Key: {api_key}")
    user = service.get_user_by_api_key(api_key)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return user


@app.post("/internal/tests/create-user")
def create_user(
    user: UserCreationSchema, response: Response, db_session: DbSessionDep
) -> UserSchema | ErrorSchema:
    try:
        service = UserService(db_session)
        created_user = service.create_user(email=user.email, password=user.password)
        if created_user is None:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"error": "User already exists"}
        return created_user
    except Exception:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"error": "Internal server error"}


@app.post("/internal/tests/get-user-data")
def fetch_api_key(
    login_data: UserLoginSchema, response: Response, db_session: DbSessionDep
) -> UserSchema | ErrorSchema:
    try:
        service = UserService(db_session)
        user_data = service.fetch_user_api_key(
            email=login_data.email, password=login_data.password
        )
        if user_data is None:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"error": "User not found or invalid credentials"}
        return user_data
    except Exception:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"error": "Internal server error"}


@app.get("/internal/health")
def health_check(response: Response):
    service = HealthCheckService()
    is_api_healthy = service.check_api_health()
    response.status_code = (
        status.HTTP_200_OK
        if all([is_api_healthy])
        else status.HTTP_503_SERVICE_UNAVAILABLE
    )
    return {
        "api": is_api_healthy,
    }


@app.post("/emotion/new")
def create_emotion(
    emotion_data: EmotionTraceCreationSchema,
    request: Request,
    response: Response,
    db_session: DbSessionDep,
    logged_user: Annotated[UserModel, Depends(get_user_by_api_key)],
) -> EmotionTraceSchema | ErrorSchema:
    try:
        service = EmotionService(db_session, logged_user)
        new_emotion = service.create_emotion(emotion_data)
        response.status_code = status.HTTP_201_CREATED
        return new_emotion
    except Exception:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"error": "Internal server error"}


@app.get("/emotion/list")
def list_emotions(
    response: Response,
    db_session: DbSessionDep,
    logged_user: Annotated[UserModel, Depends(get_user_by_api_key)],
) -> list[EmotionTraceSchema] | ErrorSchema:
    try:
        service = EmotionService(db_session, logged_user)
        emotions = service.list_emotions()
        return emotions
    except Exception:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"error": "Internal server error"}


@app.post("/financial-transaction/new")
def create_financial_transaction(
    transaction_data: FinancialTransactionCreationSchema,
    request: Request,
    response: Response,
    db_session: DbSessionDep,
    logged_user: Annotated[UserModel, Depends(get_user_by_api_key)],
) -> FinancialTransactionSchema | ErrorSchema:
    try:
        service = FinancialTransactionService(db_session, logged_user)
        new_transaction = service.create_financial_transaction(transaction_data)
        response.status_code = status.HTTP_201_CREATED
        return new_transaction
    except Exception:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"error": "Internal server error"}


@app.get("/financial-transaction/list")
def list_financial_transactions(
    response: Response,
    db_session: DbSessionDep,
    logged_user: Annotated[UserModel, Depends(get_user_by_api_key)],
) -> list[FinancialTransactionSchema] | ErrorSchema:
    try:
        service = FinancialTransactionService(db_session, logged_user)
        transactions = service.list_financial_transactions()
        return transactions
    except Exception:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"error": "Internal server error"}


@app.post("/credit-loan/new")
def create_credit_loan(
    loan_data: CreditLoanCreationSchema,
    request: Request,
    response: Response,
    db_session: DbSessionDep,
    logged_user: Annotated[UserModel, Depends(get_user_by_api_key)],
) -> CreditLoanSchema | ErrorSchema:
    try:
        service = CreditLoanService(db_session, logged_user)
        new_loan = service.create_loan(loan_data)
        response.status_code = status.HTTP_201_CREATED
        return new_loan
    except Exception:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"error": "Internal server error"}


@app.get("/credit-loan/list")
def list_credit_loans(
    request: Request,
    response: Response,
    db_session: DbSessionDep,
    logged_user: Annotated[UserModel, Depends(get_user_by_api_key)],
) -> list[CreditLoanSchema] | ErrorSchema:
    try:
        service = CreditLoanService(db_session, logged_user)
        loans = service.list_loans()
        return loans
    except Exception:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"error": "Internal server error"}
