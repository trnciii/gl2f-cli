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

	for k, v in lister.listers().items():
		p = subparsers.add_parser(k)
		lister.add_args(p)
		pretty.add_args(p)
		article.add_args(p)
		p.set_defaults(handler=make_subcommand(v))
