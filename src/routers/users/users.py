from typing import Annotated
from fastapi import APIRouter, Depends, status
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


@router.get("", status_code=status.HTTP_200_OK)
def get_all_user(db: db_dependancy):
    return db.query(Users).all()
