from app.tools.nl2sql import VannaSQLTool


def test_generate_sql_last_quarter_sales():
    tool = VannaSQLTool.__new__(VannaSQLTool)
    sql = tool.generate_sql("查询上季度销售额")
    assert "SUM(amount)" in sql
    assert "-3 months" in sql


def test_generate_sql_promotion():
    tool = VannaSQLTool.__new__(VannaSQLTool)
    sql = tool.generate_sql("分析促销活动")
    assert "is_promotion = 1" in sql
