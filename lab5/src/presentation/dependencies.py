from sqlalchemy.orm import Session
from src.common.database import SessionLocal
from src.common.event_bus import EventBus

_global_event_bus = EventBus()

def get_event_bus() -> EventBus:
    return _global_event_bus

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()