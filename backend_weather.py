from datetime import date, timedelta
from api_request import Weather_API

class GeoData():
	def __init__(self, city: str, amount_of_days: int):
		self.city = city
		self.amount_of_days = amount_of_days
		self.status_code = 0
		self.json_response = {}
		self.get_api_values()
		
		if "error" in self.json_response:
			return

		self.data = {"min_temp":[],
					 "max_temp":[],
					 "avg_temp":[],
					 "humidity":[],
					 "icon":[],
					 "location":[],
					 "current":[],
					 "days":[],
					 "image":""}

		self.parse_api_values()
		self.string_format_weekdays()
		self.get_background_image()


	def get_api_values(self) -> None:
		""" 
		fetches the API data for the given city and number of days,
		stores the response JSON in self.json_response.
		"""
		api = Weather_API(self.city, self.amount_of_days)
		self.json_response = api.get_api_json()
		self.status_code = api.status_code


	def parse_api_values(self) -> None:	
		"""
		in for loop:
		parse the json json_response into self.data,
		each list for specific json_response,
		index in each list order by days,
		i.e every index [0] in whole lists will be current day,
		every index [1] in whole lists will be tommorow, etc...
		"""

		# TODO: move for other function and explain
		self.data["current"].append(self.json_response["current"]["temp_c"])
		self.data["current"].append(self.json_response["forecast"]["forecastday"][0]["day"]["condition"]["text"])
		self.data["location"].append(self.json_response["location"]["name"])
		self.data["location"].append(self.json_response["location"]["country"])
		self.data["location"].append(self.json_response["location"]["tz_id"])
    	
		for i in range(self.amount_of_days):
			self.data["min_temp"].append(self.json_response["forecast"]["forecastday"][i]["day"]["mintemp_c"])
			self.data["max_temp"].append(self.json_response["forecast"]["forecastday"][i]["day"]["maxtemp_c"])
			self.data["avg_temp"].append(self.json_response["forecast"]["forecastday"][i]["day"]["avgtemp_c"])
			self.data["humidity"].append(self.json_response["forecast"]["forecastday"][i]["day"]["avghumidity"])
			self.data["icon"].append(self.json_response["forecast"]["forecastday"][i]["day"]["condition"]["icon"])


	def string_format_weekdays(self) -> None:
		"""
		api returns date,
		thats function make it human readable and return weekdays for client in weather.html
		"""
		current_date = date.today()

		# sets relevant days in the list
		for i in range(self.amount_of_days):
			self.data["days"].append(current_date + timedelta(days=i))


		# convert the date to weekday name i.e Sunday, Monday etc...
		for i in range(self.amount_of_days):
			self.data["days"][i] = self.data["days"][i].strftime("%A")

		self.data["days"][0] = "Today"
		try:
			self.data["days"][1] = "Tomorrow"

		finally:
			return


	def get_background_image(self) -> None:
		
		"""
		background for weather.html depend on state in user location input
		"""
		
		snow_image, rainy_image, cloudy_image, sunny_image = self.load_links()
		state = self.json_response["forecast"]["forecastday"][0]["day"]["condition"]["text"]
	
		if "rain" in state:
			self.data["image"] = rainy_image
		
		elif "snow" in state:
			self.data["image"] = snow_image

		elif "Cloudy" in state or "Overcast" in state:
			self.data["image"] = cloudy_image

		else:
			self.data["image"] = sunny_image


	@staticmethod
	def load_links() -> None:
		
		with open("background/snow.txt", "r") as snow:
			snow_image = snow.read()

		with open("background/rainy.txt", "r") as rainy:
			rainy_image = rainy.read()

		with open("background/cloudy.txt", "r") as cloudy:
			cloudy_image = cloudy.read()

		with open("background/sunny.txt", "r") as sunny:
			sunny_image = sunny.read()

		return snow_image, rainy_image, cloudy_image, sunny_image
