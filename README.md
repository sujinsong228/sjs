# 企业经营分析 Agent（RAG + Multi-Agent）

一个可直接运行的端到端 Agent Demo（默认离线、无 API Key）：
- **结构化分析**：本地 SQLite 销售数据 + NL2SQL。
- **非结构化检索**：本地 PDF/TXT/MD 文档检索。
- **多 Agent 流程**：Analyst 生成分析，Reporter 生成报告。
- **前端展示**：Streamlit 页面直接查看 SQL、证据、结论、报告。

## 1. 一键本地运行（推荐）

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app/ui/streamlit_app.py
```

打开浏览器访问：
- http://localhost:8501

> 首次运行会自动初始化 `data/sales.db`（无需手动建库）。

## 2. 环境变量（可选）

```bash
cp .env.example .env
```

常用配置：

```env
DATABASE_URI=sqlite:///./data/sales.db
DOCS_DIR=./data/docs
USE_OPENAI_API=false
```

## 3. 示例问题

- 查询上季度销售额
- 分析促销策略执行效果，并给出改进建议
- 对比促销和非促销订单的收入与折扣情况

## 4. 代码结构

```text
app/
  agents/workflow.py      # 多Agent流程（离线分析 + 报告生成）
  tools/nl2sql.py         # NL2SQL + SQLite 自动初始化
  tools/pdf_rag.py        # 本地文档切片与关键词检索
  ui/streamlit_app.py     # Streamlit 前端
  core/config.py          # 环境配置
```

## 5. 说明

- 当前版本默认离线运行，适合面试演示和本地开发。
- 如果你想切回在线 API 模式，可设置 `USE_OPENAI_API=true` 并补充对应模型调用逻辑。
