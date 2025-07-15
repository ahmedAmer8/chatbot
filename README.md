# Groq Chatbot

A simple chatbot application using Groq API with FastAPI backend and Gradio frontend.

## Features

- 🤖 AI-powered chatbot using Groq API
- 🚀 FastAPI backend with proper error handling and logging
- 💻 User-friendly Gradio web interface
- 📊 Token usage and execution time tracking
- 📝 Conversation history
- 🐳 Docker containerization for easy deployment
- 🧩 Modular code structure

## Project Structure

```
groq-chatbot/
├── api/
│   ├── __init__.py
│   ├── main.py          # FastAPI application
│   └── models.py        # Pydantic models
├── frontend/
│   ├── __init__.py
│   └── gradio_app.py    # Gradio UI
├── services/
│   ├── __init__.py
│   └── groq_client.py   # Groq API client
├── utils/
│   ├── __init__.py
│   └── logger.py        # Logging utilities
├── .env                 # Environment variables
├── config.py           # Configuration settings
├── requirements.txt    # Python dependencies
├── Dockerfile         # Docker configuration
├── docker-compose.yml # Docker Compose configuration
└── README.md          # This file
```

## Setup Instructions

### 1. Get Your Groq API Key

1. Go to [Groq Console](https://console.groq.com/)
2. Sign up or log in
3. Create a new API key
4. Copy the API key

### 2. Local Development Setup

1. **Clone or create the project structure**

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   - Copy the `.env` file and add your Groq API key:
   ```
   GROQ_API_KEY=your_actual_groq_api_key_here
   ```

4. **Run the application**
   
   **Option A: Run both services manually**
   ```bash
   # Terminal 1 - Start FastAPI backend
   python api/main.py
   
   # Terminal 2 - Start Gradio frontend
   python frontend/gradio_app.py
   ```
   
   **Option B: Use Docker**
   ```bash
   # Build and run with Docker Compose
   docker-compose up --build
   ```

### 3. Access the Application

- **Gradio UI**: http://localhost:7860
- **FastAPI Backend**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## Usage

1. Open your browser and go to http://localhost:7860
2. Type your message in the text box
3. Click "Send" or press Enter
4. View the AI response and usage statistics
5. Continue the conversation - history is maintained
6. Use "Clear Chat" to start a new conversation

## API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `POST /chat` - Chat with the AI

### Example API Request

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello, how are you?",
    "conversation_history": []
  }'
```

## Features Explanation

### For Beginners

1. **Modular Structure**: Code is organized into different folders:
   - `api/` - Backend API code
   - `frontend/` - User interface code
   - `services/` - External service integrations
   - `utils/` - Helper functions

2. **Configuration**: All settings are in `config.py` and `.env` files

3. **Logging**: Proper error tracking and logging throughout the application

4. **Error Handling**: The app gracefully handles errors and shows user-friendly messages

5. **Docker**: Easy deployment with containers

## Troubleshooting

### Common Issues

1. **"GROQ_API_KEY is required" error**
   - Make sure you've set your API key in the `.env` file

2. **Connection errors**
   - Ensure both FastAPI and Gradio are running
   - Check that ports 8000 and 7860 are available

3. **Module not found errors**
   - Run from the project root directory
   - Ensure all dependencies are installed

### Docker Issues

1. **Build fails**
   - Make sure Docker is installed and running
   - Check that all files are in the correct locations

2. **Container won't start**
   - Check Docker logs: `docker-compose logs`
   - Ensure the `.env` file has the correct API key

## Customization

### Change the AI Model
Edit `config.py` and modify the `GROQ_MODEL` variable:
```python
GROQ_MODEL = "llama3-70b-8192"  # Use a different model
```

### Modify the UI
Edit `frontend/gradio_app.py` to change the interface design

### Add New Features
- Add new endpoints in `api/main.py`
- Extend the Groq client in `services/groq_client.py`
- Modify the UI in `frontend/gradio_app.py`

## Learning Resources

This project demonstrates:
- REST API development with FastAPI
- Web UI creation with Gradio
- API integration (Groq)
- Docker containerization
- Python project structure
- Error handling and logging
- Environment configuration

## Support

If you encounter any issues:
1. Check the logs for error messages
2. Ensure all dependencies are installed
3. Verify your API key is correct
4. Make sure all services are running

Happy chatting! 🤖