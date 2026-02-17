# Backend
FROM python:3.10-slim AS backend
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Frontend
FROM node:18-alpine AS frontend
WORKDIR /frontend
COPY frontend .
RUN npm install -g serve
CMD ["serve", "-s", ".", "-l", "3000"]
