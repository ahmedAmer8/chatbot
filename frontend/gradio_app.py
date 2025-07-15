"""
Gradio frontend for the chatbot
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config
import gradio as gr
import requests
import json
from typing import List, Tuple
from utils.logger import setup_logger

logger = setup_logger(__name__)

class ChatbotUI:
    """Gradio UI for the chatbot"""
    
    def __init__(self):
        """Initialize the chatbot UI"""
        self.api_url = f"http://localhost:{Config.API_PORT}"
        self.conversation_history = []
        self.total_tokens = 0
        
    def chat_with_bot(self, message: str, history: List[Tuple[str, str]]) -> Tuple[List[Tuple[str, str]], str, str]:
        """
        Send message to chatbot and return response
        
        Args:
            message: User message
            history: Chat history from Gradio
            
        Returns:
            Tuple of (updated_history, stats, empty_string_to_clear_input)
        """
        try:
            logger.info(f"Sending message to API: {message[:50]}...")
            
            # Prepare request data
            request_data = {
                "message": message,
                "conversation_history": self.conversation_history
            }
            
            # Send request to API
            response = requests.post(
                f"{self.api_url}/chat",
                json=request_data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                bot_response = result["response"]
                tokens_used = result["tokens_used"]
                execution_time = result["execution_time"]
                
                # Update conversation history
                self.conversation_history.append({"role": "user", "content": message})
                self.conversation_history.append({"role": "assistant", "content": bot_response})
                
                # Update total tokens
                self.total_tokens += tokens_used
                
                # Update chat history for Gradio
                history.append((message, bot_response))
                
                # Create stats string
                stats = f"Tokens: {tokens_used} | Time: {execution_time:.2f}s | Total Tokens: {self.total_tokens}"
                
                logger.info(f"Received response successfully")
                return history, stats, ""
                
            else:
                error_msg = f"API Error: {response.status_code}"
                history.append((message, error_msg))
                logger.error(f"API request failed: {response.status_code}")
                return history, "Error occurred", ""
                
        except requests.exceptions.RequestException as e:
            error_msg = f"Connection Error: {str(e)}"
            history.append((message, error_msg))
            logger.error(f"Connection error: {str(e)}")
            return history, "Connection error", ""
        except Exception as e:
            error_msg = f"Unexpected Error: {str(e)}"
            history.append((message, error_msg))
            logger.error(f"Unexpected error: {str(e)}")
            return history, "Unexpected error", ""
    
    def clear_chat(self) -> Tuple[List, str, str]:
        """
        Clear chat history
        
        Returns:
            Tuple of (empty_history, empty_stats, empty_input)
        """
        self.conversation_history = []
        self.total_tokens = 0
        logger.info("Chat history cleared")
        return [], "", ""
    
    def create_interface(self) -> gr.Blocks:
        """
        Create Gradio interface
        
        Returns:
            Gradio Blocks interface
        """
        with gr.Blocks(title="Groq Chatbot") as interface:
            gr.Markdown("# 🤖 Groq Chatbot")
            gr.Markdown("Chat with AI using Groq API")
            
            with gr.Row():
                with gr.Column(scale=3):
                    chatbot = gr.Chatbot(
                        label="Chat History",
                        height=400,
                        show_label=True
                    )
                    
                    with gr.Row():
                        msg_input = gr.Textbox(
                            label="Your Message",
                            placeholder="Type your message here...",
                            lines=2,
                            scale=4
                        )
                        send_btn = gr.Button("Send", variant="primary", scale=1)
                    
                    clear_btn = gr.Button("Clear Chat", variant="secondary")
                
                with gr.Column(scale=1):
                    gr.Markdown("### 📊 Stats")
                    stats_display = gr.Textbox(
                        label="Usage Statistics",
                        value="No messages yet",
                        lines=3,
                        interactive=False
                    )
                    
                    gr.Markdown("### ℹ️ Info")
                    gr.Markdown("""
                    - **Tokens**: Number of tokens used in the last request
                    - **Time**: Execution time for the last request
                    - **Total Tokens**: Total tokens used in this session
                    """)
            
            # Event handlers
            send_btn.click(
                fn=self.chat_with_bot,
                inputs=[msg_input, chatbot],
                outputs=[chatbot, stats_display, msg_input]
            )
            
            msg_input.submit(
                fn=self.chat_with_bot,
                inputs=[msg_input, chatbot],
                outputs=[chatbot, stats_display, msg_input]
            )
            
            clear_btn.click(
                fn=self.clear_chat,
                outputs=[chatbot, stats_display, msg_input]
            )
        
        return interface
    
    def launch(self):
        """Launch the Gradio interface"""
        interface = self.create_interface()
        
        logger.info(f"Launching Gradio interface on {Config.GRADIO_HOST}:{Config.GRADIO_PORT}")
        
        interface.launch(
            server_name=Config.GRADIO_HOST,
            server_port=Config.GRADIO_PORT,
            share=True,
            debug=False
        )

if __name__ == "__main__":
    chatbot_ui = ChatbotUI()
    chatbot_ui.launch()