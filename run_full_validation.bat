@echo off
echo PDF-to-Markdown Validation System
echo ==================================
echo This will:
echo 1. Extract text from your PDF using OCR
echo 2. Compare it with Claude's Markdown output
echo 3. Generate detailed validation report
echo.
echo Press any key to start validation...
pause

cd /d "C:\Users\drewa\Claude Code\python-projects\pdf-to-markdown"
python pdf_validation_system.py

echo.
echo Validation complete! Check validation_report.txt for details.
pause