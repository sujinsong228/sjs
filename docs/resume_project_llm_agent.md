# 可放在简历中的项目：企业经营分析 Agent（RAG + Multi-Agent + NL2SQL）

> 适配岗位：大模型应用开发 / AI Agent 开发 / AI 产品工程师

## 1) 项目定位（一句话版）

基于开源技术栈构建企业经营分析 Agent：将 PDF 运营文档与 PostgreSQL 业务数据统一接入，通过多 Agent 工作流自动完成“问题理解 → 数据检索 → SQL 分析 → 结论汇报”，支持可追溯证据与可视化展示。

---

## 2) 简历可直接粘贴版本

### 项目名称
企业经营分析 Agent（RAG + Multi-Agent）

### 项目描述（2-3 行）
- 基于 **LangChain/LangGraph 思路 + Streamlit + PostgreSQL + Milvus** 搭建端到端智能分析系统，支持自然语言问答、报表生成与经营建议输出。
- 通过 **NL2SQL + 文档 RAG** 的混合检索策略，同时处理结构化与非结构化数据，解决“只会聊天不会算数”的业务落地痛点。
- 设计多 Agent 协作链路（Router/Analyst/Reporter），实现复杂问题拆解、工具调用与答案生成。

### 个人职责（示例）
- 负责 Agent 工作流与工具层设计，定义 Router 决策逻辑与错误回退机制。
- 实现 NL2SQL Tool（schema 感知 + SQL 安全校验 + 执行结果格式化）与 PDF RAG Tool（切片、向量索引、Top-K 召回）。
- 完成前端交互与 Docker 化部署，支持一键启动演示环境。
- 设计评测集并跟踪核心指标：SQL 执行成功率、检索命中率、响应延迟、业务可用率。

### 技术栈
Python, LangChain/LangGraph, OpenAI API, PostgreSQL, Milvus, Streamlit, Docker Compose

### 项目亮点（建议写 3 条）
- **混合数据推理**：结构化 SQL 结果与非结构化证据融合，回答更可解释。
- **多 Agent 可扩展架构**：可按场景新增“风控 Agent / 预测 Agent / 审计 Agent”。
- **工程化可演示**：本地容器化部署 + UI，可用于面试现场 Demo。

### 量化结果（示例，按实际替换）
- SQL 可执行率从 71% 提升到 90%+；
- 文档检索命中率提升 18%；
- 复杂问题端到端平均响应时间控制在 6s 内。

---

## 3) GitHub 开源项目结合方式（面试可讲）

你可以用“**借鉴 + 二次开发**”的方式介绍，不要说完全从零造轮子：

- 参考 Agent 编排开源思路：
  - LangChain: https://github.com/langchain-ai/langchain
  - LangGraph: https://github.com/langchain-ai/langgraph
- 参考向量数据库与检索实践：
  - Milvus: https://github.com/milvus-io/milvus
- 参考应用化落地界面：
  - Streamlit: https://github.com/streamlit/streamlit
- 参考 NL2SQL 产品化方向：
  - Vanna: https://github.com/vanna-ai/vanna

建议面试表述：
> “核心不是复现开源仓库，而是根据业务场景做取舍：我重点解决了路由策略、工具容错、结果可追溯和部署交付。”

---

## 4) 面试高频追问与回答模板

### Q1：为什么要做 Multi-Agent，而不是单 Agent？
- 单 Agent 在复杂任务里容易上下文混乱。
- 多 Agent 可以职责分离：Router 负责决策，Analyst 负责计算，Reporter 负责表达。
- 可维护性更好，后续新增能力只需要新增 Agent/Tool。

### Q2：怎么保证 SQL 安全？
- 只读账户 + 禁止 DDL/DML。
- SQL AST/关键字白名单校验。
- 超时、结果行数限制、异常兜底模板。

### Q3：如何评估效果？
- NL2SQL：可执行率、结果正确率。
- RAG：Recall@K、引用证据覆盖率。
- 业务侧：用户采纳率、任务完成时长。

---

## 5) 你可再进阶的两个方向

1. **引入记忆与反馈学习**：记录用户纠错，更新 few-shot 与路由策略。
2. **引入可观测性**：对每次 Agent 调用进行 tracing，定位延迟与失败节点。

---

## 6) 30 秒自我介绍版本（可背诵）

我做过一个企业经营分析 Agent 项目，核心是把结构化数据库和 PDF 文档统一到一个多 Agent 工作流中。系统能把自然语言问题自动拆解，按需调用 NL2SQL 和 RAG 工具，再输出可追溯的分析报告。项目用 Python + Streamlit + PostgreSQL + Milvus + Docker 落地，重点做了路由决策、SQL 安全和容错，最终达到了可演示、可部署、可迭代的工程标准。
