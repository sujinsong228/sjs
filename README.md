# 智能销售数据分析助手（Production Demo Ready）

一个可直接跑通演示的混合数据分析系统：
- **非结构化数据**：PDF 文档通过 `LangChain + Milvus` 向量检索。
- **结构化数据**：`PostgreSQL` 销售数据通过 `NL2SQL` 自动查询。
- **多 Agent 协作**：分析 Agent + 报告 Agent。
- **Agentic RAG**：先规划任务，再调用 SQL 与文档检索工具进行融合分析。
- **前端与部署**：`Streamlit` + `Docker Compose`。
- **Demo Mode**：无 OpenAI Key 时仍可离线演示完整链路（确定性 LLM 输出 + 本地检索回退）。

## 架构概览

```text
用户问题
  │
  ├── AnalystAgent
  │     ├── 生成执行计划（任务拆解）
  │     ├── NL2SQL -> PostgreSQL
  │     └── PDF RAG -> Milvus（失败时回退本地关键词检索）
  │
  ├── 融合分析结论
  └── ReportAgent 生成管理层报告
```

## 目录结构

```text
app/
  agents/workflow.py      # 多Agent与Agentic RAG编排 + DemoLLM回退
  tools/nl2sql.py         # NL2SQL(含Vanna可选) + SQL只读安全限制
  tools/pdf_rag.py        # PDF索引与向量检索(含本地回退检索)
  ui/streamlit_app.py     # 前端交互
  main.py                 # CLI演示入口
  core/config.py          # 环境配置
data/
  init.sql                # PostgreSQL 初始化样例数据
```

## 快速启动（推荐）

1. 配置环境变量

```bash
cp .env.example .env
# Demo模式可不填 OPENAI_API_KEY
```

2. 一键启动

```bash
docker compose up --build
```

3. 打开前端

- http://localhost:8501

## 本地命令行演示

```bash
python -m app.main "分析上季度促销策略执行效果，并给出改进建议"
```

## 生产增强点（本版本已覆盖）

- ✅ SQL 只读安全检查（拦截 DDL/DML）。
- ✅ Vanna 可选接入（`ENABLE_VANNA=true` + `VANNA_MODEL`）。
- ✅ PDF 检索回退机制（Milvus不可用时仍可运行演示）。
- ✅ Demo/Production 双模式。
- ✅ Docker 依赖健康检查，确保启动顺序更稳定。

## 示例问题

- 查询上季度销售额
- 分析促销策略执行效果，并给出改进建议
- 对比促销和非促销订单的收入与折扣情况
