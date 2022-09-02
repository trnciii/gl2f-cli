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


if __name__ == '__main__':
	main()