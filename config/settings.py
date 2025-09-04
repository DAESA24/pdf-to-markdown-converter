#!/usr/bin/env python3
"""
Project Configuration Settings
Centralized configuration for PDF-to-Markdown converter
"""

import os

# API Configuration
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY')

# File Paths
DEFAULT_OUTPUT_DIR = "output"
TEMP_DIR = "temp"
LOGS_DIR = "logs"

# Validation Thresholds
WORD_FIDELITY_THRESHOLD = 90.0  # Minimum acceptable word fidelity %
GRAMMAR_THRESHOLD = 80.0        # Target grammar accuracy %
FORMATTING_THRESHOLD = 85.0     # Target formatting accuracy %

# OCR Settings
DEFAULT_MAX_PAGES = 33          # Based on successful validation test
OCR_CONFIDENCE_THRESHOLD = 0.6  # Minimum OCR confidence level

# Model Settings
DEFAULT_MODEL = "claude-3-5-sonnet-20241022"
FALLBACK_MODEL = "claude-3-haiku-20240307"

# Performance Settings
MAX_TOKENS = 100000
CHUNK_SIZE = 50000

# Debug Settings
DEBUG_MODE = False
VERBOSE_LOGGING = True

def get_setting(key, default=None):
    """Get a setting value with optional default"""
    return globals().get(key, default)

def validate_environment():
    """Validate required environment variables"""
    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set")
    return True