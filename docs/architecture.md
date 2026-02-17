# System Architecture

## Overview
This project is a Public Scheme Eligibility Checker & Benefits Navigator built with:
- **Backend**: FastAPI + RAG pipeline
- **Frontend**: HTML/CSS/JS
- **Models**: Local LLM + embeddings

## Flow
1. Citizen queries via chatbot or eligibility form.
2. Backend retrieves relevant schemes using embeddings.
3. LLM generates natural language answers.
4. Frontend displays results interactively.
