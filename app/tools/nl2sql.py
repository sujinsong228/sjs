from __future__ import annotations

from typing import Any

from app.core.config import settings


class VannaSQLTool:
    """Simple NL2SQL wrapper; can be replaced by Vanna training pipeline in production."""

    def __init__(self) -> None:
        from sqlalchemy import create_engine

        self.engine = create_engine(settings.postgres_uri)

    def generate_sql(self, question: str) -> str:
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
        if "促销" in q:
            return (
                "SELECT campaign_name, SUM(amount) AS revenue, AVG(discount_rate) AS avg_discount "
                "FROM sales_orders "
                "WHERE is_promotion = TRUE "
                "GROUP BY campaign_name ORDER BY revenue DESC LIMIT 10;"
            )
        return "SELECT order_id, customer_name, amount, order_date FROM sales_orders ORDER BY order_date DESC LIMIT 20;"

    def run_sql(self, sql: str):
        import pandas as pd
        from sqlalchemy import text

        with self.engine.begin() as conn:
            return pd.read_sql(text(sql), conn)

    def query(self, question: str) -> dict[str, Any]:
        sql = self.generate_sql(question)
        df = self.run_sql(sql)
        return {"sql": sql, "rows": df.to_dict(orient="records")}
