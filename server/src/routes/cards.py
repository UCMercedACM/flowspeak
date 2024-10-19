from pydantic import BaseModel
from fastapi import APIRouter
from fastapi.responses import ORJSONResponse
from utils.request import RouteRequest

router = APIRouter(prefix="/users", tags=["Users"], default_response_class=ORJSONResponse)


@router.get(
    "/get",
    name="Get users",
)
async def get_users(request: RouteRequest) -> ORJSONResponse:
    return ORJSONResponse({"message": "hi"})
