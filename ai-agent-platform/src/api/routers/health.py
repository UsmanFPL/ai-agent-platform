from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...core.database import get_db
import redis
import os

router = APIRouter()

@router.get("/")
async def health_check():
    return {"status": "healthy", "service": "ai-agent-platform"}

@router.get("/db")
async def database_health(db: Session = Depends(get_db)):
    try:
        db.execute("SELECT 1")
        return {"status": "healthy", "component": "database"}
    except Exception as e:
        return {"status": "unhealthy", "component": "database", "error": str(e)}

@router.get("/redis")
async def redis_health():
    try:
        r = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))
        r.ping()
        return {"status": "healthy", "component": "redis"}
    except Exception as e:
        return {"status": "unhealthy", "component": "redis", "error": str(e)}