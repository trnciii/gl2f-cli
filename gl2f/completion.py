from .core import local
import os

def generate(_):
	d = local.package_data('completion.bash')
	with open(d) as f:
		print(f.read(), end='')


def add_args(parser):
	parser.set_defaults(handler=generate)
