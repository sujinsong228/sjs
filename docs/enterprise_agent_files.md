# 企业经营分析 Agent：最小可运行文件清单

下面这份就是你需要保留的“相关文件”，已经按运行优先级放在一起。

## 1) 启动与配置

1. `README.md`  
2. `.env.example`

## 2) 核心代码（只保留这个项目）

3. `app/core/config.py`
4. `app/tools/nl2sql.py`
5. `app/tools/pdf_rag.py`
6. `app/agents/workflow.py`
7. `app/ui/streamlit_app.py`

## 3) 演示数据

8. `data/docs/sample_policy.txt`

## 4) 测试（可选）

9. `tests/test_nl2sql.py`

---

## 运行方式

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
streamlit run app/ui/streamlit_app.py
```

浏览器访问：`http://localhost:8501`
