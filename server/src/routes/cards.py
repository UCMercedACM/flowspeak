from pydantic import BaseModel
from fastapi import APIRouter
from fastapi.responses import ORJSONResponse
from utils.request import RouteRequest

router = APIRouter(prefix="/cards", tags=["Cards"], default_response_class=ORJSONResponse)


@router.get(
    "/get/{id}",
    name="Get card",
)
async def get_users(request: RouteRequest, id: int) -> ORJSONResponse:
    return ORJSONResponse({"message": "hi"})
