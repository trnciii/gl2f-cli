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


def login():
	token = update(input('enter token:'))
	if token:
		print('success')
		save(token)
	else:
		print('fail')


def update_cli():
	before = load()
	after = update(before)

	if after == '':
		pass
	elif before == after:
		print('up to date')
	else:
		print('token updated')


def commands():
	return {
		'remove': remove,
		'file': lambda: print(file()),
		'load': lambda: print(load()),
		'login': login,
		'update': update_cli,
	}


def add_args(parser):
	parser.add_argument('command', type=str, choices=list(commands().keys()))
	parser.add_argument('args', nargs='*')


def auth(args):
	commands()[args.command](*args.args)


def main():
	import argparse

	parser = argparse.ArgumentParser()
	add_args(parser)
	args = parser.parse_args()

	commands()[args.command](*args.args)
