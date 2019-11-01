import requests
import base64
import datetime
import time
import random

# -------------------------------------------------
# Author: Jhonathan Davi A.K.A jh00nbr
# About-me: http://jhonathandavi.com.br
# Blog: lab.insightsecurity.com.br
# Github: github.com/jh00nbr
# Linkedin: https://www.linkedin.com/in/jhonathandavi/
# Twitter @jh00nbr
# -------------------------------------------------

# Change the ADVFN user and password.

__author__ = "Jhonathan Davi A.K.A jh00nbr"
__email__ = "jdavi@insightsecurity.com.br"
__version__ = '0.1'

stocks_bov = ['IBOV11']

def load_useragents():
    uas = []
    with open("user-agents.txt", 'rb') as uaf:
        for ua in uaf.readlines():
            if ua:
                uas.append(ua.strip()[0:-1-0])
    random.shuffle(uas)
    return uas

def get_magic_cookies():
	__urls__ = {'url_login':'https://secure.advfn.com/login/secure' }
	
	payload = {'redirect_url': base64.b64encode('https://br.advfn.com'), 'site':'br', 'login_username':'lucasalmada', 'login_password':'26990315'}
	headers = {'User-Agent': random.choice(load_useragents())}

	_req = requests.post(__urls__['url_login'], data=payload, headers=headers)

	account_login =  _req.history[0].headers['location']
	req_gsv = requests.get(account_login) # Request for get SID values in content
	cookies_l = req_gsv.history[0].cookies

	if req_gsv.history:
		SID_USER = req_gsv.history[0].cookies['SID']
		USER_COOKIES = [_ for _ in req_gsv.history[0].cookies]
		USER_REQUEST = payload['login_username']

	return cookies_l

def main():
	stocks_failed = []
	stocks_timeout =[]
	date = datetime.datetime.today()

	for stock in stocks_bov:
		req_itd = requests.get('https://br.advfn.com/p.php?pid=data&daily=0&columnheads=1&symbol={0}^{1}'.format('BOV',stock), cookies=get_magic_cookies())
		
		if "There were no results for your query" in req_itd.content:
			print("[ {0} ] Stock Failed\n".format(stock))
			stocks_failed.append(stock)
		elif "You have made too many requests. Please wait before trying to download again." in req_itd.content:
			print("[ {0} ] Stock timeout".format(stock))
			stocks_timeout.append(stock)
			time.sleep(60) #Time of 60 secounds
			pass
		else:	
			print("[ {0} ] Intraday stock :)\n".format(stock))
			with open("csv/INTRADAY_{0}_{1}_{2}-{3}.csv".format('BOV',stock, date.day, date.month), "a") as itd:
				itd.write(req_itd.content)
			itd.close()

if __name__ == '__main__':
	main()