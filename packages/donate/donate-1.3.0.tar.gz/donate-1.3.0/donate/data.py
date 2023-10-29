import random

class Data:
	def __init__(self,):
		self.list_description = ["Счет на услуги №1234", "Инвойс для оплаты", "Счет на продукцию",
								"Платеж за услуги", "Заказанные товары", "Счет за аренду", "Оплата труда",
								"Коммерческий инвойс", "Счет-фактура", "Счет для клиента"]
		self.list_hiddenMessage = ["Счет успешно оплачен.", "Платеж получен, спасибо!", "Ваш платеж подтвержден.",
									"Оплата счета завершена.", "Счет оплачен вовремя.", "Успешная транзакция.",
									"Деньги получены.", "Платеж прошел успешно.", "Операция завершена.",
									"Ваш баланс обновлен."]
		self.top_crypto = ["TONCOIN", "BOLT", "TAKE",
							"KOTE", "TNX", "AMBR"]
	def generator(self, numrange=(0.000045, 1), expiredIn=60):
		gen_data = {}

		gen_data["amount"] = random.uniform(numrange[0], numrange[1])
		gen_data["numPayments"] = 1
		gen_data["currency"] = random.choice(self.top_crypto)
		gen_data["description"] = random.choice(self.list_description)
		gen_data["hiddenMessage"] = random.choice(self.list_hiddenMessage)
		gen_data["commentsEnabled"] = False
		gen_data["callbackUrl"] = "https://t.me/ton_rocket"
		gen_data["payload"] = "some custom payload I want to see in webhook or when I request invoice"
		gen_data["expiredIn"] = expiredIn

		return gen_data