@echo off
echo Installing dependencies...
pip install -r requirements.txt
echo.
echo Starting Fitness Assistant...
echo Open http://localhost:5000 in your browser
python app.py
pause
