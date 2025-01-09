import time
from typing import Annotated

from fastapi import APIRouter, Depends, Path, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR

from app.dependencies import get_chainlink_service
from app.schemas.price import PriceResponse
from app.services.chainlink_service import ChainlinkService

router = APIRouter(prefix="/prices", tags=["Prices"])


@router.get("/nearest/{timestamp}", response_model=PriceResponse)
async def get_nearest_price(
        timestamp: Annotated[int, Path(title="Unix Timestamp", le=int(time.time()))],
        chainlink_service: Annotated[ChainlinkService, Depends(get_chainlink_service)]

):
    try:
        price = chainlink_service.get_chainlink_price_at_timestamp(timestamp)
        return {"price": price}
    except ValueError as ve:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
