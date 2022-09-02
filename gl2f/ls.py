import argparse
from .core import lister, pretty, article


def make_subcommand(core):
	def subcommand(args):
		pretty.post_argparse(args)

		fm = pretty.Formatter(f=args.format, fd=args.date_format, sep=args.sep, preview=args.preview)
		fm.reset_index(digits=len(str(args.number)))

		for i in core(args):
			if args.dl_media:
				article.save_media(i, option=args.dl_media, dump=args.dump_response)
			fm.print(i)

	return subcommand


def add_args(parser):
	subparsers = parser.add_subparsers()

	parser_blogs = subparsers.add_parser('blogs')
	lister.add_args(parser_blogs)
	pretty.add_args(parser_blogs)
	article.add_args(parser_blogs)
	parser_blogs.set_defaults(handler=make_subcommand(lister.blogs))

	parser_radio = subparsers.add_parser('radio')
	lister.add_args(parser_radio)
	pretty.add_args(parser_radio)
	article.add_args(parser_radio)
	parser_radio.set_defaults(handler=make_subcommand(lister.radio))

	parser_news = subparsers.add_parser('news')
	lister.add_args(parser_news)
	pretty.add_args(parser_news)
	article.add_args(parser_news)
	parser_news.set_defaults(handler=make_subcommand(lister.news))
