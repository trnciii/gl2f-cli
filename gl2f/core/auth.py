import os

def filepath():
	from . import local
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
	res = verify(au)
	if not res['success']:
		print('unauthorized')
		return ''

	token = res['token']
	if token != au:
		save(token)
	return token