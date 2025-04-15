from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
router = APIRouter()


class CreateUserRequest(BaseModel):
    username: str
    email: str
    firstname: str
    lastname: str
    password: str
    role: str



@router.post("/auth")
async def create_user(user: CreateUserRequest):
    return {"user": "authenticated"}
