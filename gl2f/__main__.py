import argparse
from . import blogs, auth, radio, news, ls


def main():
	parser = argparse.ArgumentParser()
	subparsers = parser.add_subparsers()


	parser_blogs = subparsers.add_parser('blogs')
	ls.add_args(parser_blogs)
	parser_blogs.set_defaults(handler=ls.make_subcommand(blogs.core))

	parser_auth = subparsers.add_parser('auth')
	auth.add_args(parser_auth)
	parser_auth.set_defaults(handler=auth.core)

	parser_radio = subparsers.add_parser('radio')
	ls.add_args(parser_radio)
	parser_radio.set_defaults(handler=ls.make_subcommand(radio.core))

	parser_news = subparsers.add_parser('news')
	ls.add_args(parser_news)
	parser_news.set_defaults(handler=ls.make_subcommand(news.core))


	args = parser.parse_args()

	if hasattr(args, 'handler'):
		args.handler(args)
	else:
		parser.print_help()


if __name__ == '__main__':
	main()