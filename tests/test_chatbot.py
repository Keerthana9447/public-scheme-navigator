import pytest
from backend.chatbot.bot import ChatBot
from backend.rag_pipeline import RAGPipeline

def test_chatbot_answer():
    rag = RAGPipeline()
    bot = ChatBot(rag)
    response = bot.answer("Tell me about pensions")
    assert "Answer" in response
