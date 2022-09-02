import argparse
from . import auth, core, opener


def main():
	parser = argparse.ArgumentParser()
	subparsers = parser.add_subparsers()


	parser_blogs = subparsers.add_parser('blogs')
	core.add_args(parser_blogs)
	parser_blogs.set_defaults(handler=core.subcommand.blogs)

	parser_auth = subparsers.add_parser('auth')
	auth.add_args(parser_auth)
	parser_auth.set_defaults(handler=auth.core)

	parser_radio = subparsers.add_parser('radio')
	core.add_args(parser_radio)
	parser_radio.set_defaults(handler=core.subcommand.radio)

	parser_news = subparsers.add_parser('news')
	core.add_args(parser_news)
	parser_news.set_defaults(handler=core.subcommand.news)

	parser_open = subparsers.add_parser('open')
	opener.add_args(parser_open)


	args = parser.parse_args()

	if hasattr(args, 'handler'):
		args.handler(args)
	else:
		parser.print_help()


if __name__ == '__main__':
	main()