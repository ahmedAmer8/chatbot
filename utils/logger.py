"""
Logging utilities for the chatbot
"""
import logging
from config import Config

def setup_logger(name: str) -> logging.Logger:
    """
    Set up a logger with the given name
    
    Args:
        name: Name of the logger
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(Config.LOG_LEVEL)
    
    # Create console handler if it doesn't exist
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setLevel(Config.LOG_LEVEL)
        
        # Create formatter
        formatter = logging.Formatter(Config.LOG_FORMAT)
        handler.setFormatter(formatter)
        
        # Add handler to logger
        logger.addHandler(handler)
    
    return logger