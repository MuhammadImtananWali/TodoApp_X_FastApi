from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from src.database.database import SessionLocal
from sqlalchemy.orm import Session
from .model import Users


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# user_dependancy = Annotated[dict, Depends(get_current_user)]
db_dependancy = Annotated[Session, Depends(get_db)]

class CreateUserRequest(BaseModel):
    email: EmailStr = Field(..., example="john@example.com")
    username: str = Field(..., example="johndoe")
    first_name: str = Field(..., example="John")
    last_name: str = Field(..., example="Doe")
    password: str = Field(..., example="StrongPassword123")
    phone_number: str = Field(..., example="+123456789")

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "john.doe@example.com",
                "username": "johndoe123",
                "first_name": "John",
                "last_name": "Doe",
                "password": "StrongPassword123",
                "phone_number": "+1234567890"
            }
        }
    }

@router.get("", status_code=status.HTTP_200_OK)
def get_all_user(db: db_dependancy):
    return db.query(Users).all()


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependancy, create_user_request: CreateUserRequest):
    user_by_email = db.query(Users).filter(Users.email == create_user_request.email).first()
    user_by_username = db.query(Users).filter(Users.username == create_user_request.username).first()
    if user_by_email or user_by_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists",
        )
    
    new_user = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        hashed_password=create_user_request.password,
        is_active=True,
        role="user",
        phone_number=create_user_request.phone_number
    )

    db.add(new_user)
    db.commit()