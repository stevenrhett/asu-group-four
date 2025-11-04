from pathlib import Path
from uuid import uuid4
import sys

import pytest_asyncio
from beanie import init_beanie
from httpx import AsyncClient, ASGITransport
from mongomock_motor import AsyncMongoMockClient
from types import ModuleType

BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

motor_module = ModuleType("motor")
motor_asyncio_module = ModuleType("motor.motor_asyncio")
motor_asyncio_module.AsyncIOMotorClient = AsyncMongoMockClient  # type: ignore[attr-defined]
motor_module.motor_asyncio = motor_asyncio_module  # type: ignore[attr-defined]
sys.modules.setdefault("motor", motor_module)
sys.modules["motor.motor_asyncio"] = motor_asyncio_module

from app.main import app  # noqa: E402
from app.models.application import Application  # noqa: E402
from app.models.job import Job  # noqa: E402
from app.models.user import User  # noqa: E402
from app.models.profile import Profile  # noqa: E402
from app.services.email import clear_email_outbox  # noqa: E402


@pytest_asyncio.fixture
async def app_client(monkeypatch):
    async def _init_db_override():
        client = AsyncMongoMockClient()
        db = client[f"job_portal_test_{uuid4().hex}"]
        await init_beanie(database=db, document_models=[User, Job, Application, Profile])

    monkeypatch.setattr("app.main.init_db", _init_db_override)

    await _init_db_override()
    clear_email_outbox()
    await app.router.startup()
    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            yield client
    finally:
        clear_email_outbox()
        await app.router.shutdown()
