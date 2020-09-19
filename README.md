# photowall

# mode dev
export FLASK_ENV=development
export DSLR_PATH="."
export EVENT_DIR=example    
flask run


# mode prod
set EVENT_DIR=OREAL
python app.py