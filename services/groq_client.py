
import time
from typing import Dict, Any
from groq import Groq
from config import Config
from utils.logger import setup_logger

logger = setup_logger(__name__)

class GroqClient:
    """Client for interacting with Groq API"""
    
    def __init__(self):
        """Initialize Groq client"""
        if not Config.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is required")
        
        self.client = Groq(api_key=Config.GROQ_API_KEY)
        self.model = Config.GROQ_MODEL
        logger.info(f"Initialized Groq client with model: {self.model}")
    
    def chat(self, message: str, conversation_history: list = None) -> Dict[str, Any]:
        """
        Send a message to Groq and get response
        
        Args:
            message: User message
            conversation_history: Previous conversation messages
            
        Returns:
            Dictionary containing response, tokens used, and execution time
        """
        try:
            start_time = time.time()
            
            messages = []
            if conversation_history:
                messages.extend(conversation_history)
            messages.append({"role": "user", "content": message})
            
            logger.info(f"Sending message to Groq: {message[:50]}...")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=1000,
                temperature=0.7
            )
            
            end_time = time.time()
            execution_time = end_time - start_time
            
            response_content = response.choices[0].message.content
            tokens_used = response.usage.total_tokens
            
            logger.info(f"Received response in {execution_time:.2f}s, tokens: {tokens_used}")
            
            return {
                "response": response_content,
                "tokens_used": tokens_used,
                "execution_time": execution_time,
                "success": True
            }
            
        except Exception as e:
            logger.error(f"Error calling Groq API: {str(e)}")
            return {
                "response": f"Sorry, I encountered an error: {str(e)}",
                "tokens_used": 0,
                "execution_time": 0,
                "success": False
            }