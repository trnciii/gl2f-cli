import argparse
from . import opener, ls, cat, dl, search
import sys, time

def board_subcommand_parsers(subparsers):
	return [
		( cmd, subparsers.add_parser(cmd.name()) )
		for cmd in [opener, ls, cat, dl, search]
	]


def ex(parser):
	args = parser.parse_args()
	if hasattr(args, 'handler'):
		args.handler(args)


def main():
	from . import auth, local
	from .core import lister, sixel

	parser = argparse.ArgumentParser()
	subparsers = parser.add_subparsers()

	parser_auth = subparsers.add_parser('auth')
	auth.add_args(parser_auth)

	local.add_args(subparsers.add_parser('local'))

	subparsers.add_parser('sixel').set_defaults(handler=lambda args:print(sixel.status))

	for c, p in board_subcommand_parsers(subparsers):
		lister.add_args_boardwise(p, c)

	ex(parser)



def make_partial(key):
	def f():
		from .core import lister
		parser = argparse.ArgumentParser()
		board = lister.listers()[key]
		for c, p in board_subcommand_parsers(parser.add_subparsers()):
			c.add_args(p, board)
		ex(parser)

	return f

class partial:
	blogs = make_partial('blogs')
	radio = make_partial('radio')
	news = make_partial('news')
	today = make_partial('today')


if __name__ == '__main__':
	main()