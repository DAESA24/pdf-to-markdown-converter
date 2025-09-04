#!/usr/bin/env python3
"""Test script to verify Python and Anthropic SDK installation."""

import sys
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")

try:
    import anthropic
    print(f"[OK] Anthropic SDK version: {anthropic.__version__}")
    print("[OK] All required packages are installed!")
    
    # Test API key setup
    import os
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if api_key:
        print(f"[OK] ANTHROPIC_API_KEY is set (length: {len(api_key)} characters)")
    else:
        print("[WARNING] ANTHROPIC_API_KEY environment variable is not set")
        print("  You can set it using: export ANTHROPIC_API_KEY='your-api-key-here'")
        print("  Or you'll be prompted for it when running the converter")
    
except ImportError as e:
    print(f"[ERROR] Error importing anthropic: {e}")
    print("  Try running: pip install anthropic")
    sys.exit(1)

print("\n[OK] Setup complete! You can now run the PDF converter:")
print("  python pdf_to_markdown_sonnet.py")