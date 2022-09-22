import os

def filepath():
	from .core import local
	return os.path.join(local.home(), 'auth')

def file():
	path = filepath()
	if os.path.exists(path):
		return path
	else:
		print('file not found')
		return None

def load():
	if path := file():
		with open(path) as f:
			return f.readline().rstrip('\n')
	else:
		return ''


def save(token):
	with open(filepath(), 'w') as f:
		f.write(token)

def remove():
	path = file()
	if path	and 'n' != input(f'removing {path} (Y/n)').lower():
		os.remove(path)


def verify(au):
	import requests
	return requests.get(
		'https://api.fensi.plus/v1/auth/token/verify',
		cookies={},
		headers={
	    'origin': 'https://girls2-fc.jp',
	    'x-authorization': au,
	    'x-from': 'https://girls2-fc.jp/page/blogs',
	    'x-root-origin': 'https://girls2-fc.jp',
		}).json()


def update(au):
	from .core import log
	import sys
	log('verifying token')

	res = verify(au)
	if not res['success']:
		print('unauthorized')
		return ''

	token = res['token']
	if token != au:
		log('token updated')
		save(token)
	return token


def set_token(token=None):
	if token == None:
		token = input('enter token:')

	if update(token):
		print('success')
		save(token)


def update_cli():
	before = load()
	after = update(before)

	if after == '':
		pass
	elif before == after:
		print('up to date')
	else:
		print('token updated')


def login():
	import json

	def find_token(log):
		for e in log:
			try:
				return json.loads(e['message'])['message']['params']['headers']['x-authorization']
			except:
				pass


	def wait_for_login_with_browser(timeout):
		from selenium import webdriver
		from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
		from webdriver_manager.chrome import ChromeDriverManager
		import time

		d = DesiredCapabilities.CHROME
		d['goog:loggingPrefs'] = {'performance':'ALL'}
		driver = webdriver.Chrome(ChromeDriverManager().install(), desired_capabilities=d)

		log_all = []
		try:
			driver.get('https://girls2-fc.jp/')
			for i in range(timeout):
				time.sleep(1)

				log = driver.get_log('performance')
				log_all.append([json.loads(e['message']) for e in log])

				token = find_token(log)
				if token != None:
					return token, log_all

			raise TimeoutError('timeout')

		finally:
			driver.quit()


	try:
		print('login with the browser opening now.')

		token, log = wait_for_login_with_browser(120)

		with open('login.json', 'w') as f:
			json.dump(log, f, indent=2)

	except Exception as e:
		print(e)
		token = input('failed to get token from a browser. enter a token ')

	set_token(token)


def commands():
	return {
		'remove': remove,
		'file': lambda: print(file()),
		'load': lambda: print(load()),
		'set-token': set_token,
		'update': update_cli,
		'login': login
	}


def add_args(parser):
	parser.add_argument('command', type=str, choices=list(commands().keys()))
	parser.add_argument('args', nargs='*')
	parser.set_defaults(
		handler = lambda args:commands()[args.command](*args.args)
	)
