import os
from tgtg import TgtgClient
from twilio.rest import Client 
import sched, time
from datetime import datetime


RESET_LIST_HOUR = 3
RESET_LIST_MINUTE = 1
cycle_seconds = 60

def send_sms(place):
	account_sid = os.environ['twilio_account_sid']  
	auth_token = os.environ['twilio_auth_token'] 
	client = Client(account_sid, auth_token) 
	 
	client.messages.create(  
		messaging_service_sid='MG667cecd619fb18b52d3910ad86ae16d8', 
	    body='TGTG in ' + place,      
	    to = os.environ['my_phone'] 
    )

	# print(message.sid)

def get_items_tgtg():
	tokens = {'access_token': os.environ['tgtg_access_token'], 
	'refresh_token': os.environ['tgtg_refresh_token'], 
	'user_id': os.environ['tgtg_user_id']}

	client = TgtgClient(access_token=tokens['access_token'], refresh_token=tokens['refresh_token'], user_id=tokens['user_id'])

	# You can then get some items, by default it will *only* get your favorites
	return client.get_items()

def do_something(sc): 
	# print("Doing stuff...")
	now = datetime.now()
	if now.hour == RESET_LIST_HOUR and now.minute < RESET_LIST_MINUTE:
		past_items.clear()

	items = get_items_tgtg()
	for item in items:
		if item['items_available']:
			if item['store']['store_name'] not in past_items:
				past_items.append(item['store']['store_name'])
				send_sms(item['store']['store_name'])

	s.enter(cycle_seconds, 1, do_something, (sc,))


s = sched.scheduler(time.time, time.sleep)
past_items = []
s.enter(5, 1, do_something, (s,))
s.run() 






