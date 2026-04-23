from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from langchain_openai import ChatOpenAI

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
        self.llm = ChatOpenAI(model=settings.openai_model, api_key=settings.openai_api_key, temperature=0)
        self.sql_tool = VannaSQLTool()
        self.rag_tool = PDFKnowledgeBase()

    def run(self, question: str) -> AnalystOutput:
        sql_result = self.sql_tool.query(question)
        evidence = self.rag_tool.search(question)

        prompt = (
            "你是一名销售分析师。结合结构化数据与文档证据，输出简明分析结论。\n"
            f"问题: {question}\n"
            f"SQL: {sql_result['sql']}\n"
            f"数据: {sql_result['rows'][:10]}\n"
            f"文档证据: {evidence}\n"
        )
        analysis = self.llm.invoke(prompt).content
        return AnalystOutput(
            sql=sql_result["sql"],
            data=sql_result["rows"],
            evidence=evidence,
            analysis=analysis,
        )


class ReportAgent:
    def __init__(self) -> None:
        self.llm = ChatOpenAI(model=settings.openai_model, api_key=settings.openai_api_key, temperature=0.2)

    def run(self, question: str, analyst_output: AnalystOutput) -> str:
        prompt = (
            "请生成一份面向销售总监的报告，包含：1) 核心结论 2) 指标解读 3) 风险 4) 下一步行动。\n"
            f"用户问题: {question}\n"
            f"分析结论: {analyst_output.analysis}\n"
            f"结构化数据: {analyst_output.data[:10]}\n"
            f"文档证据: {analyst_output.evidence}\n"
        )
        return self.llm.invoke(prompt).content


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
        }
