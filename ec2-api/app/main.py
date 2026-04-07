from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import health, install, seo

app = FastAPI(
    title="Hosted skill API",
    description="Private SEO skill — requires X-API-Key",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[],  # set via env / reverse proxy in production; empty = no browser CORS
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(install.router)
app.include_router(seo.router)


@app.get("/")
def root() -> dict[str, str]:
    return {"service": "hosted-skill-api", "docs": "/docs"}
