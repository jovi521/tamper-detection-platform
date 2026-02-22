"""Run backend: python run.py (from backend dir) or from project root: python -m uvicorn backend.app.main:app --reload."""
import sys
from pathlib import Path

# 从 backend 目录运行时，将项目根加入 path，以便 backend.app 可被解析
_root = Path(__file__).resolve().parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "backend.app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
