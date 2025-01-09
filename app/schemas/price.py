from pydantic import BaseModel


class PriceResponse(BaseModel):
    price: float
