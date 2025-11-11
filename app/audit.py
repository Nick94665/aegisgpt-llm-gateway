import time
import asyncio
from sqlalchemy import MetaData, Table, Column, Integer, String, Text, create_engine
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

from .config import settings

metadata = MetaData()
audit_table = Table(
    "audit",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("timestamp", Integer),
    Column("user", String(128)),
    Column("roles", String(256)),
    Column("redaction_summary", String(256)),
    Column("prompt_issues", String(256)),
    Column("model_response_sample", Text),
)

_engine: AsyncEngine = None

def get_engine():
    global _engine
    if _engine is None:
        _engine = create_async_engine(settings.AUDIT_DB_URL, echo=False)
    return _engine

async def init_db():
    engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

async def write_audit(user: str, roles: str, redaction_summary: str, prompt_issues: str, response_sample: str):
    engine = get_engine()
    async with engine.begin() as conn:
        await conn.execute(
            insert(audit_table).values(
                timestamp=int(time.time()), user=user, roles=roles,
                redaction_summary=redaction_summary, prompt_issues=prompt_issues,
                model_response_sample=(response_sample[:1000] if response_sample else "")
            )
        )
