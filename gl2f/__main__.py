import argparse
from . import auth, opener, ls


def main():
	parser = argparse.ArgumentParser()
	subparsers = parser.add_subparsers()

	parser_auth = subparsers.add_parser('auth')
	auth.add_args(parser_auth)
	parser_auth.set_defaults(handler=auth.core)

	parser_open = subparsers.add_parser('open')
	opener.add_args(parser_open)

	parser_ls = subparsers.add_parser('ls')
	ls.add_args(parser_ls)


	args = parser.parse_args()

	if hasattr(args, 'handler'):
		args.handler(args)
	else:
		parser.print_help()


def make_partial(board):

	def f():
		parser = argparse.ArgumentParser()
		subparsers = parser.add_subparsers()


		parser_ls = subparsers.add_parser('ls')
		ls.add_args_partially(parser_ls, board)

		parser_open = subparsers.add_parser('open')
		opener.add_args_partially(parser_open, board)


		args = parser.parse_args()

		if hasattr(args, 'handler'):
			args.handler(args)
		else:
			parser.print_help()

	return f

class partial:
	blogs = make_partial('blogs')
	radio = make_partial('radio')
	news = make_partial('news')


if __name__ == '__main__':
	main()