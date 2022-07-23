import argparse
from . import blogs
from .ls import ls, pretty

def main():
	parser = argparse.ArgumentParser()
	subparsers = parser.add_subparsers()

	parser_blogs = subparsers.add_parser('blogs')
	blogs.add_args(parser_blogs)
	parser_blogs.set_defaults(handler=blogs.ls_blogs)

	args = parser.parse_args()

	if hasattr(args, 'handler'):
		args.handler(args)
	else:
		parser.print_help()


if __name__ == '__main__':
	main()