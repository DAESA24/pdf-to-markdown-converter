@echo off
if "%ANTHROPIC_API_KEY%"=="" (
    echo Error: ANTHROPIC_API_KEY environment variable not set
    echo Please set your API key: set ANTHROPIC_API_KEY=your_key_here
    echo Or run: setx ANTHROPIC_API_KEY "your_key_here" (for permanent setting)
    pause
    exit /b 1
)
cd "%~dp0.." && C:\Users\drewa\AppData\Local\Programs\Python\Python312\python.exe -m src.converters.pdf_to_markdown_sonnet %*