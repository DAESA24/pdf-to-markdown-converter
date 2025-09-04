@echo off
echo PDF-to-Markdown Accuracy Validator
echo ===================================

REM Check if files were provided as arguments
if "%~1"=="" (
    echo Usage: validate_conversion.bat "pdf_file" "markdown_file" [output_report]
    echo.
    echo Example:
    echo validate_conversion.bat "document.pdf" "document.md" "validation_report.md"
    pause
    exit /b 1
)

if "%~2"=="" (
    echo Error: Both PDF and Markdown files must be provided
    echo Usage: validate_conversion.bat "pdf_file" "markdown_file" [output_report]
    pause
    exit /b 1
)

REM Set the API key (if needed for semantic analysis)
REM set ANTHROPIC_API_KEY=your_key_here

REM Run the validator
C:\Users\drewa\AppData\Local\Programs\Python\Python312\python.exe "%~dp0pdf_accuracy_validator.py" %*

echo.
echo Validation complete!
pause