from flask import Flask
from .main import fetch_snow_reports  # Adjust the import path accordingly
from apscheduler.schedulers.background import BackgroundScheduler

# Configure the scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(fetch_snow_reports, 'interval', hours=1)  # Runs every hour

def create_app():
    app = Flask(__name__)
    with app.app_context():
        scheduler.start()
    return app
