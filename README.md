# 智能销售数据分析助手（RAG + Multi-Agent）

一个端到端的混合数据分析系统：
- **非结构化数据**：PDF/TXT/MD 文档可离线检索（关键词召回）。
- **结构化数据**：`PostgreSQL` 销售数据通过 `NL2SQL` 自动查询。
- **多 Agent 协作**：分析 Agent + 报告 Agent，自动完成查询、分析、汇报。
- **前端与部署**：`Streamlit` 交互式界面，`Docker Compose` 一键启动。
- **离线可运行**：默认不依赖 OpenAI API（`USE_OPENAI_API=false`）。

## 架构概览

```text
用户问题
  │
  ├── Agentic Router（意图判断）
  │     ├── SQL Tool（NL2SQL -> PostgreSQL）
  │     └── Local RAG Tool（关键词检索）
  │
  ├── Analyst Agent（融合结构化结果 + 文档证据）
  └── Report Agent（生成业务报告）
```

## 目录结构

```text
app/
  agents/workflow.py      # 多Agent编排（默认离线，无需API）
  tools/nl2sql.py         # NL2SQL + SQL执行
  tools/pdf_rag.py        # 本地文档切片与关键词检索
  ui/streamlit_app.py     # 前端交互
  core/config.py          # 环境配置
data/
  init.sql                # PostgreSQL 初始化样例数据
```

## 快速启动

1. 复制环境变量

```bash
cp .env.example .env
# 默认无需 OPENAI_API_KEY
# 如需启用 API 模式：设置 USE_OPENAI_API=true 并填写 OPENAI_API_KEY
```

2. 一键启动

```bash
docker compose up --build
```

3. 打开前端

- http://localhost:8501

## 示例问题

- 查询上季度销售额
- 分析促销策略执行效果，并给出改进建议
- 对比促销和非促销订单的收入与折扣情况

## 说明

- 当前仓库中 `VannaSQLTool` 提供可运行的 NL2SQL 基线逻辑（规则+SQL执行）。
- 默认 RAG 为本地关键词检索，无需任何外部 API；适合面试演示与离线场景。
- 生产场景可将本地检索替换为向量检索与模型生成。
