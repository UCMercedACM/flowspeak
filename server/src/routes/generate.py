import asyncio

from fastapi import APIRouter
from pydantic import BaseModel

from utils.request import RouteRequest

PROMPT = "Assume the user is a non verbal person. Generate a sentence explaining what I am trying to say using the text. No more information is provided. Give me 3-5 options. Give the answer in first person. DO NOT UNDER ANY CIRCUMSTANCES MENTION THE USER IS NON VERBAL: "
router = APIRouter(tags=["generate"])


class GenerateRequest(BaseModel):
    selected_images: list[str]  # these are the image stems


@router.post("/generate-response")
async def generate_response(req: RouteRequest, gen_req: GenerateRequest):
    full_input = ", ".join(gen_req.selected_images)
    resp = asyncio.to_thread(req.app.chat.send_message(PROMPT + full_input))
    return resp
