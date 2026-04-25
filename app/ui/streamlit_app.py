import pandas as pd
import streamlit as st

from app.agents.workflow import AgenticRAGSystem
from app.core.config import settings
from app.tools.pdf_rag import PDFKnowledgeBase


st.set_page_config(page_title="智能销售数据分析助手", page_icon="📈", layout="wide")
st.title("📈 智能销售数据分析助手（RAG + Multi-Agent）")
st.caption("支持离线模式（无需 API Key）：PDF/TXT/MD 文档 + PostgreSQL 数据混合检索与自动报告")

if settings.use_openai_api:
    st.info("当前模式：API 模式（USE_OPENAI_API=true）")
else:
    st.success("当前模式：离线无 API 模式（USE_OPENAI_API=false）")

system = AgenticRAGSystem()

with st.sidebar:
    st.header("知识库")
    if st.button("导入文档（PDF/TXT/MD）"):
        count = PDFKnowledgeBase().ingest_pdfs()
        st.success(f"已导入 {count} 个文档切片")

question = st.text_area(
    "请输入业务问题",
    value="分析上季度促销策略执行效果，并给出改进建议",
    height=100,
)

if st.button("开始分析", type="primary"):
    with st.spinner("多Agent协作中..."):
        result = system.run(question)

    st.subheader("运行模式")
    st.code(result["mode"])

    st.subheader("NL2SQL")
    st.code(result["sql"], language="sql")

    st.subheader("结构化数据结果")
    st.dataframe(pd.DataFrame(result["data"]))

    st.subheader("文档证据")
    for i, e in enumerate(result["evidence"], 1):
        st.markdown(f"**证据 {i}**: {e[:400]}...")

    st.subheader("分析结论")
    st.write(result["analysis"])

    st.subheader("自动报告")
    st.write(result["report"])
