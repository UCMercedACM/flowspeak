from fastapi import APIRouter, Depends, HTTPException
from db import Database

import db
from pydantic import BaseModel
from utils.sessions import authorize, hash_password, verify_password, new_session
from db.models import User, Session, UserPassword, Collection
from db.id import generate_id
from sqlmodel import select, Field
from typing import Optional

router = APIRouter(tags=["me"])

class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/login")
async def login(
    req: LoginRequest,
    db: Database = Depends(db.use),
) -> Session:
    """
    This function logs in a user and returns a session token.
    """
    user = (await db.exec(select(User).where(User.email == req.email))).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")

    passhash = (
        await db.exec(select(UserPassword.passhash).where(UserPassword.id == user.id))
    ).one()
    if not verify_password(req.password, passhash):
        raise HTTPException(status_code=401, detail="Unauthorized")

    assert user.id is not None
    return new_session(db, user.id)


class RegisterRequest(BaseModel):
    """
    This class is used to register a new user.
    """

    email: str
    password: str
    name: str

    # bio: str


@router.post("/register")
async def register(
    req: RegisterRequest,
    db: Database = Depends(db.use),
) -> Session:
    """
    This function registers a new user and returns a session token.
    """

    async with db.begin_nested():
        user = User(**req.model_dump())
        db.add(user)

    await db.refresh(user)
    assert user.id is not None

    async with db.begin_nested():
        userpw = UserPassword(id=user.id, passhash=hash_password(req.password))
        db.add(userpw)

    return new_session(db, user.id)


class MeResponse(BaseModel):
    id: int = Field(default_factory=generate_id, primary_key=True)
    email: str
    name: str
    
    # collections: Optional[list[Collection]]


@router.get("/users/me")
async def get_self(
    db: Database = Depends(db.use),
    me_id: int = Depends(authorize),
) -> MeResponse:
    """
    This function returns the currently authenticated user.
    """
    user = (await db.exec(select(User).where(User.id == me_id))).one()
    return MeResponse(**user.model_dump())
    # collections = None
    
    # if user.collections:
        
    # group = None

    # if user.group_id is not None:
    #     group = (await db.exec(select(Group).where(Group.id == user.group_id))).one()

    # return MeResponse(**user.model_dump(), group=group)