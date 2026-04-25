from __future__ import annotations

from datetime import date, timedelta
from typing import Any

from app.core.config import settings


class VannaSQLTool:
    """Simple NL2SQL wrapper with local SQLite bootstrap for demo use."""

    def __init__(self) -> None:
        from sqlalchemy import create_engine

        self.engine = create_engine(settings.database_uri)
        self._ensure_seed_data()

    def _ensure_seed_data(self) -> None:
        from sqlalchemy import text

        create_sql = """
        CREATE TABLE IF NOT EXISTS sales_orders (
          order_id INTEGER PRIMARY KEY AUTOINCREMENT,
          customer_name TEXT NOT NULL,
          campaign_name TEXT,
          amount REAL NOT NULL,
          discount_rate REAL DEFAULT 0,
          is_promotion INTEGER DEFAULT 0,
          order_date DATE NOT NULL
        );
        """

        with self.engine.begin() as conn:
            conn.execute(text(create_sql))
            count = conn.execute(text("SELECT COUNT(*) FROM sales_orders")).scalar_one()
            if count > 0:
                return

            today = date.today()
            rows = [
                ("客户A", "春季促销", 12000, 0.15, 1, today - timedelta(days=95)),
                ("客户B", "春季促销", 8000, 0.10, 1, today - timedelta(days=88)),
                ("客户C", None, 15000, 0.00, 0, today - timedelta(days=78)),
                ("客户D", "暑期大促", 22000, 0.20, 1, today - timedelta(days=45)),
                ("客户E", None, 9000, 0.00, 0, today - timedelta(days=20)),
            ]
            insert_sql = text(
                """
                INSERT INTO sales_orders
                (customer_name, campaign_name, amount, discount_rate, is_promotion, order_date)
                VALUES (:customer_name, :campaign_name, :amount, :discount_rate, :is_promotion, :order_date)
                """
            )
            for r in rows:
                conn.execute(
                    insert_sql,
                    {
                        "customer_name": r[0],
                        "campaign_name": r[1],
                        "amount": r[2],
                        "discount_rate": r[3],
                        "is_promotion": r[4],
                        "order_date": r[5].isoformat(),
                    },
                )

    def generate_sql(self, question: str) -> str:
        q = question.lower()
        if "上季度" in q and "销售" in q:
            return (
                "SELECT ROUND(SUM(amount), 2) AS total_sales "
                "FROM sales_orders "
                "WHERE order_date >= date('now', '-3 months');"
            )
        if "促销" in q:
            return (
                "SELECT campaign_name, ROUND(SUM(amount), 2) AS revenue, "
                "ROUND(AVG(discount_rate), 4) AS avg_discount "
                "FROM sales_orders "
                "WHERE is_promotion = 1 "
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
