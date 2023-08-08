from . import local
import os, json
from ..__version__ import version

def default():
	return {
		'version': version,
		'image-size': [1000, 1000]
	}

file = lambda: os.path.join(local.home(), 'config.json')

def load():
	if os.path.isfile(file()):
		with open(file(), encoding='utf-8') as f:
			return json.loads(f.read())
	else:
		return default()

def save(data):
	with open(file(), 'w', encoding='utf-8') as f:
		f.write(json.dumps(data, indent=2, ensure_ascii=False))

config = load()
