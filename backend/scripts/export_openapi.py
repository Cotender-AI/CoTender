"""Write docs/openapi.json (the frozen API contract). CI fails if it is out of date.

python -m scripts.export_openapi            # write
python -m scripts.export_openapi --check    # exit 1 if docs/openapi.json is stale
"""

import json
import os
import sys
from pathlib import Path

from app.main import app

DOCS_DIR = Path(os.environ.get("DOCS_DIR", Path(__file__).resolve().parents[2] / "docs"))
TARGET = DOCS_DIR / "openapi.json"


def main() -> int:
    fresh = json.dumps(app.openapi(), indent=2, ensure_ascii=False) + "\n"
    if "--check" in sys.argv:
        if not TARGET.exists() or TARGET.read_text(encoding="utf-8") != fresh:
            print("docs/openapi.json is out of date: run python -m scripts.export_openapi")
            return 1
        return 0
    TARGET.write_text(fresh, encoding="utf-8")
    print(f"wrote {TARGET}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
