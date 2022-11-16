import argparse
from . import opener, ls, cat, dl, search
import sys, time


def main():
	from . import auth, local
	from .core import lister, sixel

	parser = argparse.ArgumentParser()
	subparsers = parser.add_subparsers()

	parser_auth = subparsers.add_parser('auth')
	auth.add_args(parser_auth)

	local.add_args(subparsers.add_parser('local'))

	subparsers.add_parser('sixel').set_defaults(handler=lambda args:print(sixel.status))

	for cmd in [opener, ls, cat, dl, search]:
		subsubparsers = subparsers.add_parser(cmd.name()).add_subparsers()
		for k, v in lister.listers().items():
			cmd.add_args(subsubparsers.add_parser(k), v)


	args = parser.parse_args()
	if hasattr(args, 'handler'):
		args.handler(args)


if __name__ == '__main__':
	main()