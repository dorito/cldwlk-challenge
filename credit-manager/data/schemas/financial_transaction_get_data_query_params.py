from pydantic import BaseModel


class FinancialTransactionGetDataQueryParamsSchema(BaseModel):
    limit: int = 100
