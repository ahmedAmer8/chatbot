"""
Configuration settings for the chatbot
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration"""
    
    # Groq API settings
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL = "llama3-8b-8192"  # Default Groq model
    
    # API settings
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", 8000))
    
    # Gradio settings
    GRADIO_HOST = os.getenv("GRADIO_HOST", "0.0.0.0")
    GRADIO_PORT = int(os.getenv("GRADIO_PORT", 7860))
    
    # Logging settings
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"