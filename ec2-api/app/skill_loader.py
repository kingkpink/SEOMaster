from pathlib import Path

DEFAULT_SYSTEM = """You are an expert SEO assistant. Follow structured audits and clear recommendations.
Keep answers actionable and concise unless the user asks for depth."""

# Order matches references at the end of SKILL.md so the model sees the full knowledge base.
_SKILL_APPEND_FILES: tuple[str, ...] = (
    "structured-data.md",
    "technical-seo.md",
    "indexing-errors.md",
    "multi-engine-errors.md",
    "bing-copilot-seo.md",
    "regional-engines.md",
    "audit-checklist.md",
)


def load_skill_markdown(skill_dir: Path) -> str:
    main = skill_dir / "SKILL.md"
    if not main.is_file():
        return DEFAULT_SYSTEM

    parts: list[str] = [main.read_text(encoding="utf-8")]
    for name in _SKILL_APPEND_FILES:
        path = skill_dir / name
        if path.is_file():
            parts.append(f"\n\n---\n\n## Reference: {name}\n\n")
            parts.append(path.read_text(encoding="utf-8"))
    return "".join(parts)
