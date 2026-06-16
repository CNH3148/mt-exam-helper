@echo off
echo Starting AI Study UI Backend...
echo Open your browser to http://localhost:8080/
uv run --with fastapi --with uvicorn --with pydantic --with python-multipart python server.py
pause
