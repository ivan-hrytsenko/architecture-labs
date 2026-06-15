from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.common.database import Base, engine, SessionLocal
from src.presentation.routers import router
from src.presentation.dependencies import get_event_bus
from src.analytics.acl import AnalyticsACL

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    
    event_bus = get_event_bus()
    analytics_acl = AnalyticsACL(session_factory=SessionLocal)
    analytics_acl.register_subscriptions(event_bus)
    
    yield

app = FastAPI(
    title="Farm Products Marketplace - Modular Monolith",
    version="5.0.0",
    lifespan=lifespan
)

app.include_router(router, prefix="/api/v1")