from .core import lister, pretty

def name(): return 'ls'

def subcommand(args):
	items = lister.list_contents(args)

	fm = pretty.from_args(args, items)

	for i in items:
		fm.print(i)

def add_args(parser):
	lister.add_args(parser)
	pretty.add_args(parser)
	parser.set_defaults(handler=subcommand)
