"""Write docs/erd.md (Mermaid ERD) from the SQLAlchemy models: python -m scripts.export_erd"""

import os
from pathlib import Path

from sqlalchemy import Enum

from app.core.models import Base

DOCS_DIR = Path(os.environ.get("DOCS_DIR", Path(__file__).resolve().parents[2] / "docs"))
TARGET = DOCS_DIR / "erd.md"


def main() -> None:
    lines = [
        "# Entity relationship diagram",
        "",
        "Generated from `backend/app/core/models` by `python -m scripts.export_erd`. "
        "Do not edit by hand.",
        "",
        "```mermaid",
        "erDiagram",
    ]
    rels: list[str] = []
    for table in sorted(Base.metadata.sorted_tables, key=lambda t: t.name):
        lines.append(f"  {table.name.upper()} {{")
        for col in table.columns:
            typ = col.type.name if isinstance(col.type, Enum) else type(col.type).__name__.lower()
            key = " PK" if col.primary_key else (" FK" if col.foreign_keys else "")
            lines.append(f"    {typ} {col.name}{key}")
            for fk_ in col.foreign_keys:
                parent = fk_.column.table.name
                if parent != table.name and col.name not in ("approved_by", "decided_by"):
                    rels.append(f'  {parent.upper()} ||--o{{ {table.name.upper()} : "{col.name}"')
        lines.append("  }")
    lines += [*sorted(set(rels)), "```", ""]
    TARGET.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {TARGET}")


if __name__ == "__main__":
    main()
