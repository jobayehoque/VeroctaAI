"""
Logging configuration for the application
Structured logging with different levels for different environments
"""

import logging
import sys
from flask import Flask


def init_logging(app: Flask):
    """Initialize logging configuration"""
    
    # Remove default Flask logging
    app.logger.handlers.clear()
    
    # Set logging level based on environment
    if app.config.get('DEBUG'):
        log_level = logging.DEBUG
    elif app.config.get('TESTING'):
        log_level = logging.WARNING
    else:
        log_level = logging.INFO
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)
    
    # Add handler to app logger
    app.logger.addHandler(console_handler)
    app.logger.setLevel(log_level)
    
    # Set root logger level
    logging.getLogger().setLevel(log_level)
    
    # Suppress noisy third-party loggers in production
    if not app.config.get('DEBUG'):
        logging.getLogger('werkzeug').setLevel(logging.WARNING)
        logging.getLogger('urllib3').setLevel(logging.WARNING)