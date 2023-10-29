import requests
import random

class Client:
	def __init__(self, token):
		self.data = {
			"token": token
		}
	def create(self, shop_id: int, amount: float, data: dict):
		self.data["shop_id"] = int(shop_id)
		self.data["amount"] = float(amount)
		self.data["order_id"] = random.randint(3424245, 34242451)
		self.data["data"] = data
		response = requests.post("https://lk.rukassa.is/api/v1/create", data=self.data)
		return response.json()

	def info(self, id: int, shop_id: int):
		self.data["id"] = id
		self.data["shop_id"] = shop_id
		response = requests.post("https://lk.rukassa.is/api/v1/getPayInfo", data=self.data)
		return response.json()

	def withdraw_info(self, id: int, shop_id: int):
		self.data["id"] = id
		self.data["shop_id"] = shop_id
		response = requests.post("https://lk.rukassa.is/api/v1/getWithdrawInfo", data=self.data)
		return response.json()

	def get_balance(self, email: str, password: str):
		data = {
			"email": email,
			"password": password,
		}
		response = requests.post("https://lk.rukassa.is/api/v1/getBalance", data=data)
		return response.json()

	def create_withdraw(self, email: str, password: str, way: str, wallet: str, amount: float):
		data = {
			"email": email,
			"password": password,
			"way": way,
			"wallet": wallet,
			"amount": amount
		}

		response = requests.post("https://lk.rukassa.pro/api/v1/createWithdraw", data=data)
		return response.json()

	def cancel_withdraw(self, email: str, password: str, id: int):
		data = {
			"email": email,
			"password": password,
			"id": id
		}
		response = requests.post("https://lk.rukassa.pro/api/v1/cancelWithdraw", data=data)
		return response.json()