import pytest

from app.tools.nl2sql import UnsafeSQLError, VannaSQLTool


def test_generate_sql_last_quarter_sales():
    tool = VannaSQLTool()
    sql = tool.generate_sql("查询上季度销售额")
    assert "SUM(amount)" in sql
    assert "date_trunc('quarter'" in sql


def test_generate_sql_promotion():
    tool = VannaSQLTool()
    sql = tool.generate_sql("分析促销策略执行效果")
    assert "is_promotion = TRUE" in sql
    assert "order_count" in sql


def test_enforce_readonly_blocks_mutation():
    tool = VannaSQLTool()
    with pytest.raises(UnsafeSQLError):
        tool._enforce_readonly("DELETE FROM sales_orders;")
