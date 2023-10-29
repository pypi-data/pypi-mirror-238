import inspect
import random
from datetime import timedelta
import datetime
class User:
	def __init__(self,):
		self.main_path = inspect.getfile(inspect.currentframe()).replace("user.py", "user_agents.txt")
	async def user_agent(self,):
		with open(self.main_path, "r") as file:
			user_agents = file.readlines()
		return random.choice(user_agents)

	async def timeline(self,):
		current_date = datetime.date.today()
		year = current_date.year
		month = current_date.month
		day = current_date.day
		start_time = datetime.datetime(year, month, day, 12, 0, 0)
		end_time = datetime.datetime(year, month, day, 23, 59, 0)
		current_time = start_time
		time_intervals = []
		while current_time <= end_time:
			time_intervals.append(current_time.strftime("%Y-%m-%dT%H:%M:%S"))
			current_time += timedelta(minutes=1)
		return time_intervals