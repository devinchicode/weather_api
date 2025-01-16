from datetime import date, timedelta
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
	backend = GeoData(city, int(amount_of_days))

	if "error" in backend.json_response:

		error_message = backend.json_response["error"]["message"]
		continue_message = "Press button below to return home and search again"
		
		return render_template('error.html', error_message=error_message, continue_message=continue_message),
		backend.status_code


	return render_template('weather.html', data=backend.data, amount_of_days=int(amount_of_days)), backend.status_code


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
