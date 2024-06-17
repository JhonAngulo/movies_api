from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from utils.jwt_manager import create_token
from config.database import engine, Base
from schemas.user import User

Base.metadata.create_all(bind=engine)

user_router = APIRouter()

@user_router.post("/login", tags=["Login"], response_model=dict, status_code=200)
def login(user: User) -> dict:
    if user.email == "admin@gmail.com" and user.password == "admin":
        token = create_token(user.dict())
        return JSONResponse(content={"token": token}, status_code=200)
    return JSONResponse(content={"message": "Credenciales incorrectas"}, status_code=401)
