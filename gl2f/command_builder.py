import argparse
import importlib
from functools import lru_cache
from . import auth, cat, completion, configurator, dl, local, ls, opener, search
from .ayame import sixel

builtin = [auth, cat, completion, configurator, dl, local, ls, opener, search]

def version():
	try:
		from .__version__ import __version__
		return f'gl2f {__version__}'
	except:
		return 'No version info found'

def get_addon_registrars():
	from .core.config import data as config
	ret = []
	for addon in config['addons']:
		try:
			module = importlib.import_module(addon)
			ret += module.registrars
		except ImportError:
			print(f'failed to import addon {addon}')
	return ret

import time
@lru_cache()
def build(registrars):
	t0 = time.time()
	parser = argparse.ArgumentParser()
	subparsers = parser.add_subparsers()
	tree = {
		'gl2f': subparsers
	}

	parser.add_argument('-v', '--version', action='version', version=version())
	subparsers.add_parser('sixel', description='check sixel compatibility').set_defaults(handler=lambda args:sixel.check())

	for registrar in registrars:
		parent_key, name = registrar.add_to()
		parent = tree.get(parent_key)
		if not parent:
			print(f'failed to add command {parent_key}.{name}')
			continue
		p = parent.choices[name] if name in parent.choices.keys() else parent.add_parser(name)
		sub = registrar.add_args(p)
		if sub:
			tree[f'{parent_key}.{name}'] = sub
	t1 = time.time()
	print(t1-t0)
	return parser, tree
