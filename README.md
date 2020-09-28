# photowall

# mode dev
export FLASK_ENV=development
export DSLR_PATH="."
export EVENT_DIR=example    
flask run

# install
pip install -r requirements.txt

# config
copy app_conf_example.py to app_conf.py



# mode prod
change auto_start.cmd
run auto_start.cmd