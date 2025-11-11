from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from .auth import get_current_user, create_jwt
from .sanitizer import sanitize_prompt
from .redaction import redact_pii
from .audit import init_db, write_audit
from .config import settings
import asyncio

app = FastAPI(title="AegisGPT - Secure LLM Gateway (Prototype)")

class InferenceRequest(BaseModel):
    prompt: str

class InferenceResponse(BaseModel):
    safe_prompt: str
    model_output: str
    redaction_summary: dict
    issues: list

# very small mock LLM caller (replace with real LLM integration)
def call_mock_llm(prompt: str) -> str:
    # simulate an LLM response
    return "LLM says: (simulated) Your sanitized prompt length = {}".format(len(prompt))

@app.on_event("startup")
async def startup_event():
    await init_db()

@app.post("/token")
def token_gen():
    # dev-only endpoint to generate a test JWT (NOT for prod)
    token = create_jwt({"sub": "student_a", "roles": ["user"]})
    return {"token": token}

@app.post("/infer", response_model=InferenceResponse)
async def infer(payload: InferenceRequest, user=Depends(get_current_user)):
    raw = payload.prompt

    # 1) Sanitize prompt (detect prompt-injection patterns)
    sanitized, issues = sanitize_prompt(raw)

    # 2) Redact PII
    redacted, redaction_summary = redact_pii(sanitized)

    # 3) (OPTIONAL) If issues found, optionally block or require escalation
    if issues:
        # For demo, just flag and continue. In a stricter policy we would block.
        pass

    # 4) Call LLM (mock for now)
    if settings.LLM_PROVIDER == "mock":
        model_out = call_mock_llm(redacted)
    else:
        # call actual provider (OpenAI/Vertex) — placeholder
        model_out = call_mock_llm(redacted)

    # 5) Audit log (async write)
    asyncio.create_task(write_audit(
        user=user.get("sub"),
        roles=",".join(user.get("roles", [])),
        redaction_summary=str(redaction_summary),
        prompt_issues=";".join(issues) if issues else "",
        response_sample=model_out[:1000]
    ))

    return InferenceResponse(
        safe_prompt=redacted,
        model_output=model_out,
        redaction_summary=redaction_summary,
        issues=issues
    )
