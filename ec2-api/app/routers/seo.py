from pathlib import Path

import anthropic
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from app.config import get_settings
from app.deps import require_api_key
from app.skill_loader import load_skill_markdown

router = APIRouter(prefix="/v1", tags=["seo"], dependencies=[Depends(require_api_key)])


class SeoRequest(BaseModel):
    message: str = Field(..., min_length=1, description="User task or question for the SEO skill")
    context: str | None = Field(
        default=None,
        description="Optional extra context (page HTML snippet, URL notes, etc.)",
    )


class SeoResponse(BaseModel):
    reply: str
    model: str


@router.post("/seo", response_model=SeoResponse)
def run_seo_skill(body: SeoRequest) -> SeoResponse:
    settings = get_settings()
    if not settings.anthropic_api_key:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="ANTHROPIC_API_KEY not configured",
        )

    skill_dir = Path(settings.skill_dir)
    system = load_skill_markdown(skill_dir)
    user_parts: list[str] = [body.message.strip()]
    if body.context:
        user_parts.append("\n---\nAdditional context:\n" + body.context.strip())

    client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
    msg = client.messages.create(
        model=settings.anthropic_model,
        max_tokens=settings.max_output_tokens,
        system=system,
        messages=[{"role": "user", "content": "\n".join(user_parts)}],
    )

    text_blocks: list[str] = []
    for block in msg.content:
        if block.type == "text":
            text_blocks.append(block.text)

    return SeoResponse(reply="\n".join(text_blocks).strip(), model=settings.anthropic_model)
