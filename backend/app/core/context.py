from contextvars import ContextVar
from typing import Optional
from uuid import uuid4

correlation_id_ctx: ContextVar[Optional[str]] = ContextVar("correlation_id", default=None)


def set_correlation_id(value: Optional[str] = None) -> str:
    corr_id = value or str(uuid4())
    correlation_id_ctx.set(corr_id)
    return corr_id


def get_correlation_id() -> Optional[str]:
    return correlation_id_ctx.get()
