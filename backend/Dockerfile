# 工作坊：容器内跑 Flask（默认 SQLite，可通过 M4_DATABASE_PATH 挂卷持久化）
FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]
