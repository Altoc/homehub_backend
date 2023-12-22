@echo off
:: cd /d/path/to/your/project_root  # Replace with the actual path to your project root
:: call path\to\venv\Scripts\activate  # Replace with the path to your virtual environment

uvicorn app.main:app --reload

:: Pause the script to keep the terminal window open after execution (optional)
pause

