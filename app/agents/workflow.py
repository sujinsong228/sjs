from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from app.core.config import settings
from app.tools.nl2sql import VannaSQLTool
from app.tools.pdf_rag import PDFKnowledgeBase


class SimpleLLM:
    """Deterministic fallback for production demo without external model."""

    def invoke(self, prompt: str):
        class R:
            def __init__(self, content: str):
                self.content = content

        summary = "基于结构化结果与文档证据，促销活动整体拉动收入，但存在折扣效率差异。建议保留高ROI活动并优化低效渠道。"
        return R(summary)


@dataclass
class AnalystOutput:
    plan: list[str]
    sql: str
    data: list[dict[str, Any]]
    evidence: list[str]
    analysis: str


class AnalystAgent:
    def __init__(self) -> None:
        self.llm = self._build_llm(temperature=0)
        self.sql_tool = VannaSQLTool()
        self.rag_tool = PDFKnowledgeBase()

    def _build_llm(self, temperature: float):
        if settings.demo_mode or not settings.openai_api_key:
            return SimpleLLM()
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(model=settings.openai_model, api_key=settings.openai_api_key, temperature=temperature)

    def build_plan(self, question: str) -> list[str]:
        plan = ["解析用户意图并确定指标", "执行NL2SQL查询", "执行PDF知识检索", "融合结果形成分析结论"]
        if "促销" in question:
            plan.insert(1, "聚焦促销活动维度与折扣效率")
        return plan

    def run(self, question: str) -> AnalystOutput:
        plan = self.build_plan(question)
        sql_result = self.sql_tool.query(question)
        evidence = self.rag_tool.search(question)

        prompt = (
            "你是一名销售分析师。结合结构化数据与文档证据，输出简明分析结论。\n"
            f"执行计划: {plan}\n"
            f"问题: {question}\n"
            f"SQL: {sql_result.sql}\n"
            f"数据: {sql_result.rows[:20]}\n"
            f"文档证据: {evidence[:6]}\n"
        )
        analysis = self.llm.invoke(prompt).content
        return AnalystOutput(
            plan=plan,
            sql=sql_result.sql,
            data=sql_result.rows,
            evidence=evidence,
            analysis=analysis,
        )


class ReportAgent:
    def __init__(self) -> None:
        self.llm = AnalystAgent()._build_llm(temperature=0.2)

    def run(self, question: str, analyst_output: AnalystOutput) -> str:
        prompt = (
            "请生成一份面向销售总监的报告，包含：\n"
            "1) 核心结论\n2) 指标解读\n3) 风险\n4) 下一步行动\n"
            f"用户问题: {question}\n"
            f"分析计划: {analyst_output.plan}\n"
            f"分析结论: {analyst_output.analysis}\n"
            f"结构化数据: {analyst_output.data[:20]}\n"
            f"文档证据: {analyst_output.evidence[:6]}\n"
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
            "plan": analyst_output.plan,
            "sql": analyst_output.sql,
            "data": analyst_output.data,
            "evidence": analyst_output.evidence,
            "analysis": analyst_output.analysis,
            "report": report,
        }
