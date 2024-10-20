from pydantic import BaseModel
from fastapi import APIRouter, Depends
from typing import Optional
import db
from db import Database
from fastapi.responses import ORJSONResponse
from utils.request import RouteRequest
from sqlmodel import select, col
from typing import Sequence 
from db.models import Card
router = APIRouter(tags=["Cards"])




