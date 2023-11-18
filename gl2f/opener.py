from .core import lister, pretty
from .ayame import terminal as term

def name(): return 'open'

def open_url(i):
	import webbrowser
	from .core import board
	webbrowser.register("termux-open '%s'", None)
	webbrowser.open(board.content_url(i), new=0, autoraise=True)


def subcommand(args):
	items = lister.list_contents(args)
	fm = pretty.from_args(args, items)

	if args.all:
		for i in items:
			fm.print(i)
			open_url(i)
	elif args.pick:
		for i in (items[i-1] for i in args.pick if 0<i<=len(items)):
			fm.print(i)
			open_url(i)
	else:
		for i in term.selected(items, fm.format):
			open_url(i)

def add_to():
	return 'gl2f', 'open'

def add_args(parser):
	lister.add_args(parser)
	pretty.add_args(parser)
	parser.set_defaults(format='author:title')
	parser.add_argument('-a', '--all', action='store_true',
		help='open all items')
	parser.add_argument('--pick', type=int, nargs='+',
		help='select articles to show')

	parser.set_defaults(handler=subcommand)

def set_compreply():
	return '__gl2f_complete_boards'
