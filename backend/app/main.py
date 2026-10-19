from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.core.config import get_settings
from app.core.db import engine
from app.core.errors import register_error_handlers
from app.core.logging import configure_logging
from app.modules.audit.router import router as audit
from app.modules.auth.router import router as auth
from app.modules.boq.router import router as boq
from app.modules.checklist.router import router as checklist
from app.modules.documents.router import router as documents
from app.modules.exports.router import router as exports
from app.modules.jobs.router import router as jobs
from app.modules.notifications.router import router as notifications
from app.modules.organisation.router import router as organisation
from app.modules.suppliers.router import router as suppliers
from app.modules.tenders.router import router as tenders
from app.modules.usage.router import router as usage

settings = get_settings()
configure_logging(settings.log_level)

app = FastAPI(title="IntelTPS API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
register_error_handlers(app)

api = APIRouter(prefix="/api/v1")
for module_router in (
    auth,
    organisation,
    tenders,
    documents,
    jobs,
    checklist,
    boq,
    suppliers,
    exports,
    audit,
    usage,
    notifications,
):
    api.include_router(module_router)
app.include_router(api)


@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
    """Liveness: the process is up. Does not touch the database."""
    return {"status": "ok"}


@app.get("/health/ready", tags=["health"])
def ready() -> dict[str, str]:
    """Readiness: the database answers."""
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"status": "ok", "database": "ok"}
