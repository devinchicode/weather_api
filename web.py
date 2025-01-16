from datetime import date, timedelta
import requests
from flask import Flask, render_template, request
from backend_weather import GeoData

app = Flask(__name__)


@app.get('/')
def get_location():
	return render_template('index.html')


@app.route('/weather', methods=["POST"])
def weather():
	city = request.form["city"]
	amount_of_days = request.form["forecast_days"]
	data = GeoData(city, int(amount_of_days))

	if "error" in data.parameters:
		error_message = data.parameters["error"]["message"]
		continue_message = "Press button below to return home and search again"
		return render_template('error.html', error_message=error_message, continue_message=continue_message), data.status_code

	return render_template('weather.html',
	icon=data.icon, image=data.image, location=data.location,
	days=data.days, min_temp=data.min_temp, max_temp=data.max_temp,
	avg_temp=data.avg_temp, humidity=data.humidity, amount_of_days=data.amount_of_days, current=data.current)


@app.errorhandler(404)
def page_not_found(error_message):
	continue_message = "Press button below to return home and search for forecast"
	return render_template('error.html', error_message=error_message, continue_message=continue_message), 404


@app.errorhandler(500)
def server_error(error_message):
	continue_message = "Press button below to return home and search again"
	return render_template('error.html', error_message=error_message, continue_message=continue_message), 500



if __name__ == "__main__":
	app.run()
