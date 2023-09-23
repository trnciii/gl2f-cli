from .core import auth

def set_token(token=None):
	if token == None:
		token = input('enter token:')

	if auth.update(token):
		print('success')
		auth.save(token)


def update_cli():
	before = auth.load()
	if not before:
		return
	after = auth.update(before)

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
		'remove': auth.remove,
		'file': lambda: print(auth.file()),
		'load': lambda: print(auth.load()),
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
