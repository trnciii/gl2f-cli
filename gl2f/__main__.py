import argparse
from . import opener, ls, cat, dl, search, completion
import sys, time


def main():
	from . import auth, local
	from .core import lister
	from .ayame import sixel

	parser = argparse.ArgumentParser()
	subparsers = parser.add_subparsers()

	parser_auth = subparsers.add_parser('auth')
	auth.add_args(parser_auth)

	local.add_args(subparsers.add_parser('local'))

	subparsers.add_parser('sixel').set_defaults(handler=lambda args:sixel.check())

	completion.add_args(subparsers.add_parser('completion'))

	for cmd in [cat, dl, ls, opener, search]:
		cmd.add_args(subparsers.add_parser(cmd.name()))


	args = parser.parse_args()
	if hasattr(args, 'handler'):
		args.handler(args)


if __name__ == '__main__':
	main()