from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from app.core.config import settings
from app.tools.nl2sql import VannaSQLTool
from app.tools.pdf_rag import PDFKnowledgeBase


@dataclass
class AnalystOutput:
    sql: str
    data: list[dict[str, Any]]
    evidence: list[str]
    analysis: str


class AnalystAgent:
    def __init__(self) -> None:
        self.sql_tool = VannaSQLTool()
        self.rag_tool = PDFKnowledgeBase()

    def _build_analysis(self, question: str, rows: list[dict[str, Any]], evidence: list[str]) -> str:
        if not rows:
            return "当前未检索到结构化数据，请先检查数据库连接与查询条件。"

        numeric_keys = [
            k
            for k, v in rows[0].items()
            if isinstance(v, (int, float)) and not isinstance(v, bool)
        ]
        stats = []
        for key in numeric_keys[:3]:
            vals = [r[key] for r in rows if isinstance(r.get(key), (int, float))]
            if vals:
                stats.append(f"{key}均值{sum(vals)/len(vals):.2f}，最大{max(vals):.2f}，最小{min(vals):.2f}")

        evidence_brief = "；".join(e[:80].replace("\n", " ") for e in evidence[:2]) if evidence else "暂无文档证据"
        stats_text = "；".join(stats) if stats else "未发现可计算的数值指标"

        return (
            f"问题：{question}\n"
            f"数据观察：共返回{len(rows)}条记录，{stats_text}。\n"
            f"文档观察：{evidence_brief}。\n"
            "建议：优先聚焦高折扣低收益的活动，结合复购与客单价做分层优化。"
        )

    def run(self, question: str) -> AnalystOutput:
        sql_result = self.sql_tool.query(question)
        evidence = self.rag_tool.search(question)
        analysis = self._build_analysis(question, sql_result["rows"], evidence)
        return AnalystOutput(
            sql=sql_result["sql"],
            data=sql_result["rows"],
            evidence=evidence,
            analysis=analysis,
        )


class ReportAgent:
    def run(self, question: str, analyst_output: AnalystOutput) -> str:
        top_rows = analyst_output.data[:5]
        evidence = analyst_output.evidence[:2]
        return (
            "# 销售分析报告\n\n"
            f"## 1) 核心结论\n{analyst_output.analysis}\n\n"
            f"## 2) 指标样本\n{top_rows}\n\n"
            f"## 3) 风险提示\n{('证据不足，建议补充文档。' if not evidence else '部分结论来自样本文档，请业务侧复核。')}\n\n"
            "## 4) 下一步行动\n"
            "- 建立活动级毛利看板，按周监控。\n"
            "- 对高折扣活动做 A/B 测试并设置止损阈值。\n"
            "- 为重点客户群补充定向触达策略。"
        )


class AgenticRAGSystem:
    def __init__(self) -> None:
        self.analyst = AnalystAgent()
        self.reporter = ReportAgent()

    def run(self, question: str) -> dict[str, Any]:
        analyst_output = self.analyst.run(question)
        report = self.reporter.run(question, analyst_output)
        return {
            "sql": analyst_output.sql,
            "data": analyst_output.data,
            "evidence": analyst_output.evidence,
            "analysis": analyst_output.analysis,
            "report": report,
            "mode": "offline-no-api" if not settings.use_openai_api else "api",
        }
