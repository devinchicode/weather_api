import requests

class Weather_API():
	def __init__(self, city: str, amount_of_days: int):
		self.CITY = city
		self.AMOUNT_OF_DAYS = amount_of_days
		self.status_code = 0

	def get_api_json(self) -> dict:
		"""
		takes api key from api_key.txt thats should be in same dir
		send get requests and get json, converts to nested dicts,
		parsed in backend module
		"""
		with open("api_key.txt", "r") as file:
			API_KEY = file.readline()

		url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={self.CITY}&days={self.AMOUNT_OF_DAYS}&aqi=no&alerts=no"
		response = requests.get(url)
		parameters = response.json()
		self.status_code = response.status_code

		return parameters


