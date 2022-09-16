from .core import lister, pretty

def name(): return 'ls'

def add_args(parser, board):
	lister.add_args(parser)
	pretty.add_args(parser)

	def subcommand(args):
		pretty.post_argparse(args)

		fm = pretty.Formatter(f=args.format, fd=args.date, sep=args.sep)
		fm.reset_index(digits=len(str(args.number)))

		for i in lister.listers()[board](args):
			fm.print(i)

	parser.set_defaults(handler=subcommand)
