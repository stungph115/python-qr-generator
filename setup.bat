@echo off

:: Check if Python is installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python before running this script.
    exit /b
)

:: Install required packages
echo Installing required packages...
pip install -r requirements.txt

echo Setup completed. You can now run the script using 'qr-gen.py'.
pause
