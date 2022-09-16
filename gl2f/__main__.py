import argparse
from . import opener, ls, cat, dl


def board_subcommand_parsers(subparsers):
	return [
		( cmd, subparsers.add_parser(cmd.name()) )
		for cmd in [opener, ls, cat, dl]
	]


def ex(parser):
	args = parser.parse_args()
	if hasattr(args, 'handler'):
		args.handler(args)
	else:
		parser.print_help()


def main():
	from . import auth, inspect
	from .core import lister

	parser = argparse.ArgumentParser()
	subparsers = parser.add_subparsers()

	parser_auth = subparsers.add_parser('auth')
	auth.add_args(parser_auth)

	p = subparsers.add_parser('local')
	inspect.add_args(p)


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