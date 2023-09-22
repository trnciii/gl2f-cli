from . import local
import os
from ..__version__ import version

def default():
	return {
		'version': version,
		'max-image-size': [1000, 1000],
		'serve-port': 7999,
	}

def filepath():
	return os.path.join(local.home(), 'config.json')

def load():
	import json
	path = filepath()
	if os.path.isfile(path):
		with open(path, encoding='utf-8') as f:
			return json.loads(f.read())
	return {}

def save(data):
	import json
	with open(filepath(), 'w', encoding='utf-8') as f:
		f.write(json.dumps(data, indent=2, ensure_ascii=False))

config = {**default(), **load()}
