from fastapi import FastAPI
from src.routers import users_router
from src.database.database import engine, Base

# Create an instance of the FastAPI class
app = FastAPI()

# Include the routers
app.include_router(users_router)

Base.metadata.create_all(bind=engine)
