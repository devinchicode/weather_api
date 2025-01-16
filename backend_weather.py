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


		snow_image = "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/783a8afb-3bb2-4d9f-b81e-0f0a4ecce927/d4h55ea-2d48d5ab-704d-4efe-97dc-2e594087969e.gif?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcLzc4M2E4YWZiLTNiYjItNGQ5Zi1iODFlLTBmMGE0ZWNjZTkyN1wvZDRoNTVlYS0yZDQ4ZDVhYi03MDRkLTRlZmUtOTdkYy0yZTU5NDA4Nzk2OWUuZ2lmIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.CPIGkrjjdCcy_ZOSFSNUszHlEPtjQN6KXKrU3euaJH8"

		rainy_image = "https://cdna.artstation.com/p/assets/images/images/025/801/090/original/sean-lewis-sean-lewis-toonorth-loop-1000px.gif?1586964127"
		
		cloudy_image = "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/2530d3be-5b7d-4ce9-b28f-63520c8b7042/d7y567t-9072c940-5cda-4f1b-bab5-1bf98bc1ed9e.gif?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcLzI1MzBkM2JlLTViN2QtNGNlOS1iMjhmLTYzNTIwYzhiNzA0MlwvZDd5NTY3dC05MDcyYzk0MC01Y2RhLTRmMWItYmFiNS0xYmY5OGJjMWVkOWUuZ2lmIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.w72UWJFjMp1wvdUD5P6k87xe3sN0DZEWDB7z5nhhs9w"
		
		sunny_image = "https://i.pinimg.com/originals/17/00/09/170009ce70039c9a6c900f9e61759d88.gif"
		
		state = self.parameters["forecast"]["forecastday"][0]["day"]["condition"]["text"]
	
		if "rain" in state:
			self.image = rainy_image
		
		elif "snow" in state:
			self.image = snow_image

		elif "Cloudy" in state or "Overcast" in state:
			self.image = cloudy_image

		else:
			self.image = sunny_image
	
