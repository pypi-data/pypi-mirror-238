import requests
import random
from .exceptions import check_exceptions


class Client:
	def __init__(self, api_key: str = None, user_agent: str = None, proxies: dict = None):

		if proxies == None:
			pass
		elif type(proxies) is dict:
			pass
		else:
			pass
		if user_agent == None:
			self.headers = {
				"accept": "application/json",
				"Rocket-Pay-Key": api_key,
				"Content-Type": "application/json",
			}
		else:
			self.headers = {
				"accept": "application/json",
				"Rocket-Pay-Key": api_key,
				"Content-Type": "application/json",
				"User-Agent": user_agent,
			}
	def version(self, dict_mode: bool = True):
		response = requests.get("https://pay.ton-rocket.com/version", headers=self.headers).json()
		if dict_mode:
			return response
		else:
			return response.get("version")
	def info(self,):
		response = requests.get("https://pay.ton-rocket.com/app/info", headers=self.headers)
		if response.status_code not in [200, 201]:
			check_exceptions(code=response.status_code)
		else:
			return response.json()

	def transfer(self, data: dict = {}):
		"""
		options in data:
			{
			"tgUserId": 5968878656,
			"currency": "TONCOIN",
			"amount": 1.23,
			"description": "test"
			}
		"""
		data["transferId"] = str(random.randint(1000000000000, 9000000000000))
		response = requests.post("https://pay.ton-rocket.com/app/transfer", headers=self.headers, json=data)
		if response.status_code not in [200, 201]:
			check_exceptions(code=response.status_code, **response.json())
		else:
			return response.json()

	def withdrawal(self, data: dict = {}):
		"""
		options in data:
			{
				"network": "TON",
				"address": "EQB1cmpxb3R-YLA3HLDV01Rx6OHpMQA_7MOglhqL2CwJx_dz",
				"currency": "TONCOIN",
				"amount": 1.23,
				"withdrawalId": "abc-def",
				"comment": "You are awesome!"
			}
		"""
		data["withdrawalId"] = str(random.randint(1000000000000, 9000000000000))
		response = requests.post("https://pay.ton-rocket.com/app/withdrawal", headers=self.headers, json=data)
		if response.status_code not in [200, 201]:
			check_exceptions(code=response.status_code, **response.json())
		else:
			return response.json()
		
	def create(self, data: dict = {}):
		"""
			{
			"amount": 1.23,
			"numPayments": 1,
			"currency": "TONCOIN",
			"description": "best thing in the world, 1 item",
			"hiddenMessage": "thank you",
			"commentsEnabled": False,
			"callbackUrl": "https://t.me/ton_rocket",
			"payload": "some custom payload I want to see in webhook or when I request invoice",
			"expiredIn": 0
			}
		"""
		response = requests.post("https://pay.ton-rocket.com/tg-invoices", headers=self.headers, json=data)
		if response.status_code not in [200, 201]:
			check_exceptions(code=response.status_code, **response.json())
		else:
			return response.json()

	def get_me(self,):
		response = requests.get("https://pay.ton-rocket.com/tg-invoices?limit=100&offset=0", headers=self.headers)
		if response.status_code not in [200, 201]:
			check_exceptions(code=response.status_code, **response.json())
		else:
			return response.json()

	def check(self, id: int = 0):
		response = requests.get(f"https://pay.ton-rocket.com/tg-invoices/{id}", headers=self.headers)
		if response.status_code not in [200, 201]:
			check_exceptions(code=response.status_code, **response.json())
		else:
			return response.json()

	def delete(self, id: int = 0):
		response = requests.delete(f"https://pay.ton-rocket.com/tg-invoices/{id}", headers=self.headers)
		if response.status_code not in [200, 201]:
			check_exceptions(code=response.status_code, **response.json())
		else:
			return response.json()