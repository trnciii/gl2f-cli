import argparse
from . import blogs, auth, radio
from .ls import ls, pretty

def main():
	parser = argparse.ArgumentParser()
	subparsers = parser.add_subparsers()


	parser_blogs = subparsers.add_parser('blogs')
	blogs.add_args(parser_blogs)
	parser_blogs.set_defaults(handler=blogs.core)

	parser_auth = subparsers.add_parser('auth')
	auth.add_args(parser_auth)
	parser_auth.set_defaults(handler=auth.core)

	parser_radio = subparsers.add_parser('radio')
	radio.add_args(parser_radio)
	parser_radio.set_defaults(handler=radio.core)

	args = parser.parse_args()

	if hasattr(args, 'handler'):
		args.handler(args)
	else:
		parser.print_help()


if __name__ == '__main__':
	main()