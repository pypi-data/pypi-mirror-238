import aiohttp
import asyncio
import time
import random
from threading import Thread
import asyncio
import os
from ..exceptions import check_exceptions
from .user import User

async def checker(headers, id, data, func):
	os.environ['PYTHONWARNINGS'] = "ignore::RuntimeWarning"
	x = 0
	flag = False
	result = 0
	if 60 > int(data.get("expiredIn")):
		flag = "Error"

	while x < int(data.get("expiredIn")):
		if flag == "Error":
			break
		x = x + 1
		await asyncio.sleep(1)
		new_user_agent = await User().user_agent()
		headers["User-Agent"] = new_user_agent.replace("\n", "")
		timeline = await User().timeline()
		params = {"launchtime": random.choice(timeline)}
		async with aiohttp.ClientSession() as session:
			async with session.get(f"https://pay.ton-rocket.com/tg-invoices/{id}", headers=headers, params=params) as response:
				response_data = await response.json()
		if response_data.get("data").get("status") == "paid":
			flag = True
			break
	if flag == False:
		result = await func(api_key=headers.get("Rocket-Pay-Key"), status=False)
		return result
	elif flag == True:
		result = await func(api_key=headers.get("Rocket-Pay-Key"), status=response_data.get("data").get("status"), user_id=response_data.get("data").get("payments")[0].get("userId"))
		return result
	else:
		async with aiohttp.ClientSession() as session:
			async with session.delete(f"https://pay.ton-rocket.com/tg-invoices/{id}", headers=headers) as response:
				response_data = await response.json()
		check_exceptions(code=60)
		
class Donate_init:
	def __init__(self, api_key, data):
		self.headers = {
			"accept": "application/json",
			"Rocket-Pay-Key": api_key,
			"Content-Type": "application/json",
		}
		self.data = data
		self.api_key = api_key

	def __call__(self, func):
		async def wrapper(*args, **kwargs):
			new_user_agent = await User().user_agent()
			self.headers["User-Agent"] = new_user_agent.replace("\n", "")
			timeline = await User().timeline()
			params = {"launchtime": random.choice(timeline)}
			async with aiohttp.ClientSession() as session:
				async with session.post("https://pay.ton-rocket.com/tg-invoices", headers=self.headers, json=self.data, params=params) as response:
					get_data_invoice = await response.json()

			result = await func(*args, **kwargs, api_key=self.api_key, data=self.data, new_data=get_data_invoice)  # Передать аргументы в функцию
			await checker(self.headers,get_data_invoice.get("data").get("id"), self.data, func)
			return result
		return wrapper