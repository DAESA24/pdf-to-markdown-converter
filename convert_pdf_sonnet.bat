@echo off
if "%ANTHROPIC_API_KEY%"=="" (
    echo Error: ANTHROPIC_API_KEY environment variable not set
    echo Please set your API key: set ANTHROPIC_API_KEY=your_key_here
    echo Or run: setx ANTHROPIC_API_KEY "your_key_here" (for permanent setting)
    pause
    exit /b 1
)
C:\Users\drewa\AppData\Local\Programs\Python\Python312\python.exe "%~dp0pdf_to_markdown_sonnet.py" %*