# 智能销售数据分析助手（RAG + Multi-Agent）

一个端到端的混合数据分析系统：
- **非结构化数据**：PDF 文档通过 `LangChain + Milvus` 进行向量化检索。
- **结构化数据**：`PostgreSQL` 销售数据通过 `NL2SQL` 自动查询。
- **多 Agent 协作**：分析 Agent + 报告 Agent，自动完成查询、分析、汇报。
- **前端与部署**：`Streamlit` 交互式界面，`Docker Compose` 一键启动。

## 架构概览

```text
用户问题
  │
  ├── Agentic Router（意图判断）
  │     ├── SQL Tool（NL2SQL -> PostgreSQL）
  │     └── PDF RAG Tool（Embedding -> Milvus）
  │
  ├── Analyst Agent（融合结构化结果 + 文档证据）
  └── Report Agent（生成业务报告）
```

## 目录结构

```text
app/
  agents/workflow.py      # 多Agent与Agentic RAG编排
  tools/nl2sql.py         # NL2SQL + SQL执行
  tools/pdf_rag.py        # PDF索引与向量检索
  ui/streamlit_app.py     # 前端交互
  core/config.py          # 环境配置
data/
  init.sql                # PostgreSQL 初始化样例数据
```

## 快速启动

1. 复制环境变量

```bash
cp .env.example .env
# 填写 OPENAI_API_KEY
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

- 当前仓库中 `VannaSQLTool` 提供了可运行的 NL2SQL 基线逻辑（规则+SQL执行），便于演示端到端链路。
- 生产场景可将 `generate_sql` 替换为 Vanna 的训练/推理流程，与企业 schema 与历史问答结合以提升 SQL 准确率。
