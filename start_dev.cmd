@echo off
set /p EVENT_DIR="ENTER EVENT NAME: "
set EVENT_DIR
set FLASK_ENV=development
python app.py
cd C:\Users\gumpy1\Documents\GitHub\photowall\
python C:\Users\gumpy1\Documents\GitHub\photowall\app.py