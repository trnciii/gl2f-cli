from .core import config
import os

def view():
	import json
	with open(config.file(), encoding='utf-8') as f:
		print(f.read())

def create():
	if os.path.isfile(config.file()):
		print('file already exits. abort.')
		return

	config.save(config.default())
	print(f'created "{config.file()}".')

def add_args(parser):
	sub = parser.add_subparsers()

	sub.add_parser('create').set_defaults(handler=lambda _:create())
	sub.add_parser('path').set_defaults(handler=lambda _:print(config.file()))
	sub.add_parser('view').set_defaults(handler=lambda _:view())