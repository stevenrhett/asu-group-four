from contextlib import asynccontextmanager
import json
import logging
from typing import Any, Dict

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.api.v1.routes.applications import router as applications_router
from app.api.v1.routes.auth import router as auth_router
from app.api.v1.routes.inbox import router as inbox_router
from app.api.v1.routes.jobs import router as jobs_router
from app.api.v1.routes.metrics import router as metrics_router
from app.api.v1.routes.performance import router as performance_router
from app.api.v1.routes.recommendations import router as recommendations_router
from app.api.v1.routes.scheduling import router as scheduling_router
from app.api.v1.routes.search import router as search_router
from app.api.v1.routes.uploads import router as uploads_router
from app.core import compat  # noqa: F401
from app.core.context import get_correlation_id, set_correlation_id
from app.db.init_db import init_db

logger = logging.getLogger("job_portal")


def setup_logging() -> None:
    if logger.handlers:
        return

    handler = logging.StreamHandler()

    class JsonFormatter(logging.Formatter):
        def format(self, record: logging.LogRecord) -> str:
            payload: Dict[str, Any] = {
                "level": record.levelname,
                "message": record.getMessage(),
                "logger": record.name,
            }
            correlation = get_correlation_id()
            if correlation:
                payload["correlation_id"] = correlation
            if record.exc_info:
                payload["exception"] = self.formatException(record.exc_info)
            return json.dumps(payload)

    handler.setFormatter(JsonFormatter())
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        corr_id = request.headers.get("X-Correlation-ID")
        corr_id = set_correlation_id(corr_id)
        request.state.correlation_id = corr_id
        response = await call_next(request)
        response.headers["X-Correlation-ID"] = corr_id
        return response


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    await init_db()
    yield


app = FastAPI(title="Job Portal API", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(CorrelationIdMiddleware)

# Add performance monitoring middleware (ST-013)
from app.middleware.performance import PerformanceMonitoringMiddleware
app.add_middleware(PerformanceMonitoringMiddleware)


@app.middleware("http")
async def request_logging_middleware(request: Request, call_next):
    logger.info(
        json.dumps(
            {
                "event": "request_start",
                "method": request.method,
                "path": request.url.path,
            }
        )
    )
    try:
        response = await call_next(request)
        logger.info(
            json.dumps(
                {
                    "event": "request_complete",
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": response.status_code,
                }
            )
        )
        return response
    except Exception:
        logger.exception("request_failed")
        raise


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("unhandled_error")
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "correlation_id": get_correlation_id(),
        },
    )


@app.get("/health")
async def health():
    return {"status": "ok"}


app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(search_router, prefix="/api/v1/jobs", tags=["search"])
app.include_router(jobs_router, prefix="/api/v1/jobs", tags=["jobs"])
app.include_router(applications_router, prefix="/api/v1/applications", tags=["applications"])
app.include_router(scheduling_router, prefix="/api/v1/scheduling", tags=["scheduling"])
app.include_router(uploads_router, prefix="/api/v1/uploads", tags=["uploads"])
app.include_router(recommendations_router, prefix="/api/v1/recommendations", tags=["recommendations"])
app.include_router(inbox_router, prefix="/api/v1/inbox", tags=["inbox"])
app.include_router(metrics_router, prefix="/api/v1", tags=["metrics"])
app.include_router(performance_router, prefix="/api/v1", tags=["performance"])
