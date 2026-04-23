import pandas as pd
import streamlit as st

from app.agents.workflow import AgenticRAGSystem
from app.core.config import settings
from app.tools.pdf_rag import PDFKnowledgeBase


st.set_page_config(page_title="智能销售数据分析助手", page_icon="📈", layout="wide")
st.title("📈 智能销售数据分析助手（RAG + Multi-Agent）")
st.caption("支持 PDF 文档 + PostgreSQL 数据库混合检索与自动报告生成")
st.info(f"当前模式：{'Demo可离线演示' if settings.demo_mode else 'Production（需要模型与基础设施）'}")

system = AgenticRAGSystem()

with st.sidebar:
    st.header("知识库")
    if st.button("导入 PDF 到知识库"):
        try:
            count = PDFKnowledgeBase().ingest_pdfs()
            st.success(f"已导入 {count} 个文档切片")
        except Exception as exc:
            st.error(f"导入失败: {exc}")

question = st.text_area(
    "请输入业务问题",
    value="分析上季度促销策略执行效果，并给出改进建议",
    height=100,
)

if st.button("开始分析", type="primary"):
    with st.spinner("多Agent协作中..."):
        try:
            result = system.run(question)
        except Exception as exc:
            st.exception(exc)
            st.stop()

    st.subheader("Agent执行计划")
    st.write(result["plan"])

    st.subheader("NL2SQL")
    st.code(result["sql"], language="sql")

    st.subheader("结构化数据结果")
    st.dataframe(pd.DataFrame(result["data"]))

    st.subheader("文档证据")
    if result["evidence"]:
        for i, e in enumerate(result["evidence"], 1):
            st.markdown(f"**证据 {i}**: {e[:500]}...")
    else:
        st.warning("未检索到文档证据，请先导入PDF或检查Milvus连接")

    st.subheader("分析结论")
    st.write(result["analysis"])

    st.subheader("自动报告")
    st.write(result["report"])
