from datetime import date, timedelta
from api_request import Weather_API

class GeoData():
	def __init__(self, city: str, amount_of_days: int):
		self.city = city
		self.amount_of_days = amount_of_days
		self.status_code = 0
		self.parameters = []
		self.get_api_values()
		
		if "error" in self.parameters:
			return

		self.min_temp = []
		self.max_temp = []
		self.avg_temp = []
		self.humidity = []
		self.location = []
		self.icon = []
		self.current = []
		self.image = ""
		self.days = []

		self.parse_api_values()
		self.string_format_weekdays()
		self.get_background_image()


	def get_api_values(self) -> None:
		api = Weather_API(self.city, self.amount_of_days)
		self.parameters = api.get_api_json()
		self.status_code = api.status_code


	def parse_api_values(self) -> None:	
		"""
		parse the json parameters into lists,
		each list for specific parameters,
		index in each list order by days,
		i.e every index [0] in whole lists will be current day,
		every index [1] in whole lists will be tommorow, etc...
		"""
		self.current.append(self.parameters["current"]["temp_c"])
		self.current.append(self.parameters["forecast"]["forecastday"][0]["day"]["condition"]["text"])
		self.location.append(self.parameters["location"]["name"])
		self.location.append(self.parameters["location"]["country"])
		self.location.append(self.parameters["location"]["tz_id"])
    	
		for i in range(self.amount_of_days):
			self.min_temp.append(self.parameters["forecast"]["forecastday"][i]["day"]["mintemp_c"])
			self.max_temp.append(self.parameters["forecast"]["forecastday"][i]["day"]["maxtemp_c"])
			self.avg_temp.append(self.parameters["forecast"]["forecastday"][i]["day"]["avgtemp_c"])
			self.humidity.append(self.parameters["forecast"]["forecastday"][i]["day"]["avghumidity"])
			self.icon.append(self.parameters["forecast"]["forecastday"][i]["day"]["condition"]["icon"])


	def string_format_weekdays(self) -> None:
		"""
		api returns date,
		thats function make it human readable and return weekdays for client in weather.html
		"""
		current_date = date.today()

		for i in range(self.amount_of_days):
			self.days.append(current_date + timedelta(i))

		for i in range(self.amount_of_days):
			self.days[i] = self.days[i].strftime("%A")

		self.days[0] = "Today"
		try:
			self.days[1] = "Tomorrow"

		finally:
			return


	def get_background_image(self) -> None:
		
		"""
		background for weather.html depend on state in user location input
		"""
	
		with open("background/snow.txt", "r") as snow:
			snow_image = snow.read()

		with open("background/rainy.txt", "r") as rainy:
			rainy_image = rainy.read()

		with open("background/cloudy.txt", "r") as cloudy:
			cloudy_image = cloudy.read()

		with open("background/sunny.txt", "r") as sunny:
			sunny_image = sunny.read()

		state = self.parameters["forecast"]["forecastday"][0]["day"]["condition"]["text"]
	
		if "rain" in state:
			self.image = rainy_image
		
		elif "snow" in state:
			self.image = snow_image

		elif "Cloudy" in state or "Overcast" in state:
			self.image = cloudy_image

		else:
			self.image = sunny_image
	
