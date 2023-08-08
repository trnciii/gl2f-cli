import os

class Warn_once:
	printed = set()

	@staticmethod
	def print(message):
		from ..ayame import terminal as term
		if message not in Warn_once.printed:
			print(term.mod(message, term.color('yellow'), term.inv(), term.bold()))
			Warn_once.printed.add(message)

def filepath():
	from . import local
	return os.path.join(local.home(), 'auth')

def file():
	path = filepath()
	if os.path.exists(path):
		return path
	else:
		Warn_once.print('authorization info not found')
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


first_unauthorized = True
def verify(au):
	import requests
	res = requests.get(
		'https://api.fensi.plus/v1/auth/token/verify',
		cookies={},
		headers={
	    'origin': 'https://girls2-fc.jp',
	    'x-authorization': au,
	    'x-from': 'https://girls2-fc.jp/page/blogs',
	    'x-root-origin': 'https://girls2-fc.jp',
		}).json()
	if res['success']:
		return res['token']
	else:
		Warn_once.print('unauthorized')
		return None

def update(au):
	token = verify(au)
	if not token:
		return ''

	if token != au:
		save(token)
	return token
