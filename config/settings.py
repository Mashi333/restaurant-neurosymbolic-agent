import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Set to "local" to use the local Llama model, "mock" to use static responses, or an OpenAI model name
LLM_MODE = os.getenv("LLM_MODE", "local")   # "local" | "mock" | "gpt-3.5-turbo"

# HuggingFace model name for local mode
LOCAL_MODEL_ID = os.getenv("LOCAL_MODEL_ID", "meta-llama/Llama-3.2-3B-Instruct")

USE_MOCK_LLM = LLM_MODE == "mock"
