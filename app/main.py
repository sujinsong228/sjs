from __future__ import annotations

import argparse
import json

from app.agents.workflow import AgenticRAGSystem


def main() -> None:
    parser = argparse.ArgumentParser(description="Agentic RAG sales analysis demo runner")
    parser.add_argument("question", nargs="?", default="查询上季度销售额")
    args = parser.parse_args()

    result = AgenticRAGSystem().run(args.question)
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
