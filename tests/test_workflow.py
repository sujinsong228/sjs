from app.agents.workflow import AnalystAgent


def test_build_plan_for_promotion_question():
    agent = AnalystAgent()
    plan = agent.build_plan("分析促销策略执行效果")
    assert any("促销" in p for p in plan)
    assert "执行NL2SQL查询" in plan
