@echo off
echo PDF-to-Markdown Quality Analyzer
echo =================================

REM Check if markdown file was provided as argument
if "%~1"=="" (
    echo Usage: analyze_quality.bat "markdown_file" [output_report] [estimated_pages]
    echo.
    echo Example:
    echo analyze_quality.bat "document.md" "quality_report.md" 25
    pause
    exit /b 1
)

REM Run the quality analyzer
C:\Users\drewa\AppData\Local\Programs\Python\Python312\python.exe "%~dp0pdf_markdown_quality_analyzer.py" %*

echo.
echo Quality analysis complete!
pause