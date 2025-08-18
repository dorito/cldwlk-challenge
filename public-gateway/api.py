import uuid
from typing import Annotated, Union

from fastapi import Depends, FastAPI, Response, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.logger import LOGGER
from app.database import ENGINE
from data.schemas import UserCreationSchema, UserSchema, UserLoginSchema, ErrorSchema, EmotionTraceSchema, EmotionTraceCreationSchema, FinancialTransactionCreationSchema, FinancialTransactionSchema, CreditLoanCreationSchema, CreditLoanSchema 
from services import HealthCheckService, UserService, EmotionService, CreditLoanService, FinancialTransactionService
from data.models import UserModel

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
            raise Exception(f"Unauthorized for {api_key}")
        return user

@app.post("/tests/create-user")
def create_user(user: UserCreationSchema, response: Response, db_session: DbSessionDep) -> UserSchema | ErrorSchema:
    try:
        service = UserService(db_session)
        created_user = service.create_user(
            email=user.email, password=user.password
        )
        return created_user
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": str(e)}

@app.post("/tests/fetch-api-key")
def fetch_api_key(login_data: UserLoginSchema, response: Response, db_session: DbSessionDep) -> UserSchema | ErrorSchema:
    try:
        service = UserService(db_session)
        user_data = service.fetch_user_api_key(
            email=login_data.email, password=login_data.password
        )
        if user_data is None:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"error": "User not found or invalid credentials"}
        return user_data
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": str(e)}


@app.get("/health")
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
def create_emotion(emotion_data: EmotionTraceCreationSchema, request: Request, response: Response, db_session: DbSessionDep, logged_user: Annotated[UserModel, Depends(get_user_by_api_key)]) -> EmotionTraceSchema | ErrorSchema:
    try:
        service = EmotionService(db_session, logged_user)
        new_emotion = service.create_emotion(emotion_data)
        response.status_code = status.HTTP_201_CREATED
        return new_emotion
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": str(e)}

@app.get("/emotion/list")
def list_emotions(response: Response, db_session: DbSessionDep, logged_user: Annotated[UserModel, Depends(get_user_by_api_key)]) -> list[EmotionTraceSchema] | ErrorSchema:
    try:
        service = EmotionService(db_session, logged_user)
        emotions = service.list_emotions()
        return emotions
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": str(e)}

@app.post("/financial-transaction/new")
def create_financial_transaction(transaction_data: FinancialTransactionCreationSchema, request: Request, response: Response, db_session: DbSessionDep, logged_user: Annotated[UserModel, Depends(get_user_by_api_key)]) -> FinancialTransactionSchema | ErrorSchema:
    try:
        service = FinancialTransactionService(db_session, logged_user)
        new_transaction = service.create_financial_transaction(transaction_data)
        response.status_code = status.HTTP_201_CREATED
        return new_transaction
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": str(e)}

@app.get("/financial-transaction/list")
def list_financial_transactions(response: Response, db_session: DbSessionDep, logged_user: Annotated[UserModel, Depends(get_user_by_api_key)]) -> list[FinancialTransactionSchema] | ErrorSchema:
    try:
        service = FinancialTransactionService(db_session, logged_user)
        transactions = service.list_financial_transactions()
        return transactions
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": str(e)}

@app.post("/credit-loan/new")
def create_credit_loan(loan_data: CreditLoanCreationSchema, request: Request, response: Response, db_session: DbSessionDep, logged_user: Annotated[UserModel, Depends(get_user_by_api_key)]) -> CreditLoanSchema | ErrorSchema:
    try:
        service = CreditLoanService(db_session, logged_user)
        new_loan = service.create_loan(loan_data)
        response.status_code = status.HTTP_201_CREATED
        return new_loan
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": str(e)}

@app.get("/credit-loan/list")
def list_credit_loans(request: Request, response: Response, db_session: DbSessionDep, logged_user: Annotated[UserModel, Depends(get_user_by_api_key)]) -> list[CreditLoanSchema] | ErrorSchema:
    try:
        service = CreditLoanService(db_session, logged_user)
        loans = service.list_loans()
        return loans
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": str(e)}
    