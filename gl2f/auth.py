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


def login(dump=False):
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
		import time

		DesiredCapabilities.CHROME['goog:loggingPrefs'] = {'performance':'ALL'}
		driver = webdriver.Chrome()

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

		if dump:
			with open('login.json', 'w') as f:
				json.dump(log, f, indent=2)

	except Exception as e:
		print(e)
		token = input('failed to get token from a browser. enter a token ')

	set_token(token)


def add_args(parser):
	sub = parser.add_subparsers()

	sub.add_parser('file').set_defaults(handler=lambda _:print(auth.file()))

	p = sub.add_parser('login')
	p.add_argument('--dump', action='store_true')
	p.set_defaults(handler=lambda args: login(dump=args.dump))

	sub.add_parser('load').set_defaults(handler=lambda _:print(auth.load()))
	sub.add_parser('remove').set_defaults(handler=lambda _:auth.remove())

	p = sub.add_parser('set-token')
	p.add_argument('token', nargs='?', type=str)
	p.set_defaults(handler=lambda args:set_token(args.token))

	sub.add_parser('update').set_defaults(handler=lambda _:update_cli())
