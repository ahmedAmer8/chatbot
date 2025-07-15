"""
FastAPI backend for the chatbot
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from api.models import ChatRequest, ChatResponse
from services.groq_client import GroqClient
from utils.logger import setup_logger

logger = setup_logger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Groq Chatbot API",
    description="A simple chatbot API using Groq",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Groq client
try:
    groq_client = GroqClient()
    logger.info("Groq client initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Groq client: {e}")
    groq_client = None

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Groq Chatbot API is running!"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "groq_client": "connected" if groq_client else "disconnected"
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat endpoint
    
    Args:
        request: Chat request containing message and conversation history
        
    Returns:
        Chat response with AI response, tokens used, and execution time
    """
    try:
        if not groq_client:
            raise HTTPException(
                status_code=503, 
                detail="Groq client not available"
            )
        
        logger.info(f"Received chat request: {request.message[:50]}...")
        
        # Convert conversation history to dict format
        conversation_history = []
        if request.conversation_history:
            conversation_history = [
                {"role": msg.role, "content": msg.content} 
                for msg in request.conversation_history
            ]
        
        # Get response from Groq
        result = groq_client.chat(
            message=request.message,
            conversation_history=conversation_history
        )
        
        return ChatResponse(**result)
        
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Internal server error: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    from config import Config
    
    uvicorn.run(
        "main:app",
        host=Config.API_HOST,
        port=Config.API_PORT,
        reload=True
    )