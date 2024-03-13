from .core import lister, pretty, util
from .ayame import terminal as term

def subcommand(args):
	items, _ = lister.list_contents(args)

	fm = pretty.from_args(args, items)
	if args.paging == 'never':
		for i in items:
			fm.print(i, encoding=args.encoding)
	else:
		term.scroll(map(fm.format, items), eof=lambda:'')


def add_to():
	return 'gl2f', 'ls'

def add_args(parser):
	parser.description = 'List pages'

	lister.add_args(parser)
	pretty.add_args(parser)
	util.add_paging_args(parser)
	parser.set_defaults(handler=subcommand)
	parser.add_argument('--encoding')

def set_compreply():
	return '__gl2f_complete_list_args'
