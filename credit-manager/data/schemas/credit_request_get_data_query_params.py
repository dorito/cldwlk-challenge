from pydantic import BaseModel


class CreditRequestGetDataQueryParamsSchema(BaseModel):
    limit: int = 100
