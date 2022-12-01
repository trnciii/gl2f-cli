from .core import lister, pretty

def name(): return 'ls'

def subcommand(args):
	fm = pretty.from_args(args)
	fm.reset_index(digits=len(str(args.number)))

	for i in lister.list_contents(args):
		fm.print(i)

def add_args(parser):
	lister.add_args(parser)
	pretty.add_args(parser)
	parser.set_defaults(handler=subcommand)
