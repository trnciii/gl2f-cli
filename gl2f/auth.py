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


def add(token):
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
	if res['success']:
		if res['token'] != au:
			add(res['token'])
		return res['token']
	else:
		print('unauthorized')
		return False

updated = lambda: update(load())


def login():
	token = update(input('enter token:'))
	if token:
		add(token)
		return 'success'
	else:
		return 'fail'


def auth():
	import argparse

	commands = {
		'add': add,
		'remove': remove,
		'verify': lambda: verify(load()),
		'file': file,
		'load': load,
		'login': login,
	}

	parser = argparse.ArgumentParser()

	parser.add_argument('command', type=str, choices=list(commands.keys()))
	parser.add_argument('args', nargs='*')

	args = parser.parse_args()


	ret = commands[args.command](*args.args)
	print(ret)
