@echo off
cd /d "%~dp0"
".venv\Scripts\python.exe" -m streamlit run frontend/streamlit_app.py --server.port 8501 --server.address localhost --server.headless true > streamlit.server.log 2>&1
