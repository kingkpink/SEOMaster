from fastapi import Header, HTTPException, status

from app.config import get_settings, parse_api_key_set


async def require_api_key(x_api_key: str | None = Header(default=None)) -> None:
    settings = get_settings()
    allowed = parse_api_key_set(settings.api_keys)
    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="API_KEYS not configured on server",
        )
    if not x_api_key or x_api_key not in allowed:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing X-API-Key",
        )
