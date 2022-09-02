import argparse
from .core import lister, pretty, article

def name(): return 'ls'

def add_args(parser, board):
	lister.add_args(parser)
	pretty.add_args(parser)
	article.add_args(parser)

	def subcommand(args):
		pretty.post_argparse(args)

		fm = pretty.Formatter(f=args.format, fd=args.date_format, sep=args.sep, preview=args.preview)
		fm.reset_index(digits=len(str(args.number)))

		for i in lister.listers()[board](args):
			if args.dl_media:
				article.save_media(i, option=args.dl_media, dump=args.dump_response)
			fm.print(i)

	parser.set_defaults(handler=subcommand)
