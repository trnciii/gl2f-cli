import os

def filepath():
	return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'auth')

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
	res = verify(au)
	if not res['success']:
		print('unauthorized')
		return ''

	token = res['token']
	if token != au:
		save(token)
	return token


def set_token(token=None):
	if token == None:
		token = update(input('enter token:'))
	if token:
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
	from selenium import webdriver
	from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
	from webdriver_manager.chrome import ChromeDriverManager
	import json
	import time

	def find_token(log):
		for e in log:
			try:
				return json.loads(e['message'])['message']['params']['headers']['x-authorization']
			except:
				pass


	def wait_finding_token(driver, timeout):
		dump = []
		start = time.time()

		driver.get('https://girls2-fc.jp/')
		while True:
			time.sleep(1)

			log = driver.get_log('performance')
			dump.append([json.loads(e['message']) for e in log])

			token = find_token(log)
			if token != None:
				return token, dump

			if time.time() - start > timeout:
				print('timeout')
				return None, dump


	try:
		print('login with the browser opening now.')

		d = DesiredCapabilities.CHROME
		d['goog:loggingPrefs'] = {'performance':'ALL'}
		driver = webdriver.Chrome(ChromeDriverManager().install(), desired_capabilities=d)

		token, dump = wait_finding_token(driver, 120)

		driver.close()

		with open('login.json', 'w') as f:
			json.dump(dump, f, indent=2)

	except:
		token = input('failed to open a browser. enter a token ')

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


def core(args):
	commands()[args.command](*args.args[1:])


def main():
	import argparse

	parser = argparse.ArgumentParser()
	add_args(parser)
	args = parser.parse_args()

	core(args)
