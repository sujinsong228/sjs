from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from app.core.config import settings


@dataclass
class SQLResult:
    sql: str
    rows: list[dict[str, Any]]


class UnsafeSQLError(ValueError):
    pass


class VannaSQLTool:
    """NL2SQL tool with safe fallback and optional Vanna integration."""

    def __init__(self) -> None:
        self._engine = None

    @property
    def engine(self):
        if self._engine is None:
            from sqlalchemy import create_engine

            self._engine = create_engine(settings.postgres_uri)
        return self._engine

    def generate_sql(self, question: str) -> str:
        if settings.enable_vanna:
            sql = self._generate_with_vanna(question)
            if sql:
                return self._enforce_readonly(sql)

        return self._enforce_readonly(self._generate_rule_based(question))

    def _generate_with_vanna(self, question: str) -> str | None:
        try:
            from vanna.remote import VannaDefault
        except Exception:
            return None

        if not settings.vanna_model:
            return None

        vn = VannaDefault(model=settings.vanna_model, api_key=settings.openai_api_key)
        return vn.generate_sql(question)

    def _generate_rule_based(self, question: str) -> str:
        q = question.lower()
        if "上季度" in q and "销售" in q:
            return (
                "SELECT date_trunc('quarter', order_date) AS quarter, "
                "SUM(amount) AS total_sales "
                "FROM sales_orders "
                "WHERE order_date >= date_trunc('quarter', CURRENT_DATE) - interval '3 month' "
                "AND order_date < date_trunc('quarter', CURRENT_DATE) "
                "GROUP BY 1 ORDER BY 1 DESC LIMIT 1;"
            )
        if "促销" in q and ("效果" in q or "策略" in q or "执行" in q):
            return (
                "SELECT campaign_name, "
                "SUM(amount) AS revenue, "
                "AVG(discount_rate) AS avg_discount, "
                "COUNT(*) AS order_count "
                "FROM sales_orders "
                "WHERE is_promotion = TRUE "
                "GROUP BY campaign_name "
                "ORDER BY revenue DESC LIMIT 20;"
            )
        if "非促销" in q or "对比" in q:
            return (
                "SELECT is_promotion, COUNT(*) AS order_count, SUM(amount) AS total_revenue, "
                "AVG(discount_rate) AS avg_discount "
                "FROM sales_orders GROUP BY is_promotion ORDER BY is_promotion DESC;"
            )
        return (
            "SELECT order_id, customer_name, campaign_name, amount, discount_rate, "
            "is_promotion, order_date "
            "FROM sales_orders ORDER BY order_date DESC LIMIT 50;"
        )

    def _enforce_readonly(self, sql: str) -> str:
        normalized = sql.strip().lower()
        banned = ["insert ", "update ", "delete ", "drop ", "alter ", "truncate ", "create "]
        if any(token in normalized for token in banned):
            raise UnsafeSQLError("Only read-only SQL is allowed.")
        if not normalized.startswith("select") and " with " not in f" {normalized} ":
            raise UnsafeSQLError("Only SELECT/CTE queries are allowed.")
        return sql

    def run_sql(self, sql: str):
        import pandas as pd
        from sqlalchemy import text

        with self.engine.begin() as conn:
            return pd.read_sql(text(sql), conn)

    def query(self, question: str) -> SQLResult:
        sql = self.generate_sql(question)
        df = self.run_sql(sql)
        return SQLResult(sql=sql, rows=df.to_dict(orient="records"))
