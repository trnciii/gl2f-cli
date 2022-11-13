from .core import lister, pretty

def name(): return 'ls'

def add_args(parser, list_board):
	lister.add_args(parser)
	pretty.add_args(parser)

	def subcommand(args):
		fm = pretty.from_args(args)
		fm.reset_index(digits=len(str(args.number)))

		for i in list_board(args):
			fm.print(i)

	parser.set_defaults(handler=subcommand)
