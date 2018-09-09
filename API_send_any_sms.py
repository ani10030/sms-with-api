import requests
import json

def forward_to_api(url,mobile,message,api_key,flash,count):
	payload = {'senderId': 'FSTSMS', 'mobile': mobile, 'message': message, 'flash': flash}
	headers = {'Authorization': api_key}
	print '\n-- Trying to send SMS via API ['+str(count)+'] --'
	
	response = requests.request("POST", url, data=payload, headers=headers)
	if response.json()['return'] != True:
		return False
	print '<< '+response.json()['message']+' >>'
	return response.json()['return']

def forward_to_paid_api(url,mobile,message,api_key,flash,count):
	headers = {'cache-control': "no-cache"}
	querystring = {"authorization":api_key,"sender_id":"FSTSMS","message":message,"language":"english","route":"p","numbers":mobile,"flash":flash}
	print '\n-- Trying to send SMS via Paid API ['+str(count)+'] --'
	
	response = requests.request("GET", url, headers=headers, params=querystring)
	print '<< '+response.json()['message']+' >>'
	return response.json()['return']

def send_sms(sms_data):
	phone = sms_data[0]
	message = sms_data[1]

	allowed_sms_length = 149
	#Trim Message length to 160-11 = 149 characters#
	if len(message) > allowed_sms_length:
		message = message[0:145]
		message+='[..]'

	print '--> Sending SMS to '+str(phone)

	number = str(phone)
	api_keys = ["API key1", # Your free msgs API key
				"API key2"] # Your paid msgs API key

	url = "https://www.fast2sms.com/api/sms/free"
	for key in api_keys:
		count = api_keys.index(key)+1
		if api_keys.index(key)>1:
			url = "https://www.fast2sms.com/dev/bulk"
			sent_status = forward_to_paid_api(url,number,message,key,0,count)
		else:
			sent_status = forward_to_api(url,number,message,key,0,count)
		if sent_status:
			return 'SUCCESS'
		else:
			print '-- SMS was not sent. Retrying... --'
			continue
	if sent_status == False:
		return 'ERROR'