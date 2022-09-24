import argparse
from . import opener, ls, cat, dl
import sys, time
from .core.local import log

def board_subcommand_parsers(subparsers):
	return [
		( cmd, subparsers.add_parser(cmd.name()) )
		for cmd in [opener, ls, cat, dl]
	]


def ex(parser):
	log(sys.argv)
	args = parser.parse_args()
	if hasattr(args, 'handler'):
		t0 = time.time()
		args.handler(args)
		t1 = time.time()
		log(f'time {t1-t0}')


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



def make_partial(board):
	def f():
		parser = argparse.ArgumentParser()
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