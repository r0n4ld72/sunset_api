from chalice import Chalice
import requests
import json
from datetime import datetime
from pytz import timezone    

eur = timezone('Europe/Amsterdam')
eur_time = datetime.now(eur)
eur_time_format = eur_time.strftime('%Y-%m-%dT%H:%M:%S+00:00')

app = Chalice(app_name='sunset_api')
app.debug = True

@app.route('/')
def index():
    return {'response': 'ok'}


@app.route('/sunset')
def is_dark():
	response = requests.get("https://api.sunrise-sunset.org/json?lat=51.8423973&lng=4.6395056&formatted=0")
	sunset_data = response.json() 
	sunset_time = sunset_data['results']['nautical_twilight_end']
	sunrise_time = sunset_data['results']['civil_twilight_begin']
	return {'current_time': eur_time_format, 'sunrise': sunrise_time,'sunset': sunset_time, 'past_sunset': eur_time_format > sunset_time, 'before_sunrise': eur_time_format < sunrise_time,'is_dark': ((eur_time_format > sunset_time) or (eur_time_format < sunrise_time))}