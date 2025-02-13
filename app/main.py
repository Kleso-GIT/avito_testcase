from fastapi import FastAPI
from app.routers import users, auth
from app.database import engine, Base

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)

Base.metadata.create_all(bind=engine)
