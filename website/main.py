from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
from apscheduler.schedulers.background import BackgroundScheduler

def get_snow_report(url):
    try:
        r = requests.get(url)
        r.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(r.content, 'html.parser')  # Changed from 'html5lib'
        RawInfo = soup.find_all('ul', class_='vList vList_1')
        output = []
        for i in range(4, 8):
            output.append(RawInfo[i].find('span', class_="js-measurement").string)
        return output
    except Exception as e:
        print(f"Error fetching snow report from {url}: {e}")
        return []

def fetch_snow_reports():
    global sugar_loaf_snow, sunday_river_snow
    sugar_loaf_snow = get_snow_report("https://www.sugarloaf.com/mountain-report")
    sunday_river_snow = get_snow_report("https://www.sundayriver.com/mountain-report")

def create_app():
    app = Flask(__name__)

    # Fetch snow reports when the app starts
    fetch_snow_reports()

    # Configure the scheduler to fetch snow reports every hour
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_snow_reports, 'interval', hours=1)
    scheduler.start()

    @app.route('/')
    def index():
        global sugar_loaf_snow, sunday_river_snow
        # Render the template with snow reports
        return render_template('index.html', sugar_loaf_snow=sugar_loaf_snow, sunday_river_snow=sunday_river_snow)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
