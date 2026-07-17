from fastapi import APIRouter
import time

from src.api.database import get_db_row_counts

router = APIRouter(tags=["Health"])

START_TIME = time.time()


@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "version": "1.0.0",
        "uptime_seconds": round(time.time() - START_TIME, 2),
        "db_row_counts": get_db_row_counts(),
    }