from fastapi import FastAPI
from src.infrastructure.database import engine, Base
from src.presentation.routers import router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Farm Products Marketplace")
app.include_router(router)