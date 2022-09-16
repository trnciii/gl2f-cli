from .core import lister

def name(): return 'open'

def open_url(i):
	import webbrowser
	from .core import board
	webbrowser.open(board.content_url(i), new=0, autoraise=True)


def add_args(parser, board):
	lister.add_args(parser)
	parser.add_argument('-a', '--all', action='store_true',
		help='open all items')


	def subcommand(args):
		from .core import pretty, terminal as term

		items = lister.listers()[board](args)
		fm = pretty.Formatter(f='date-p:author:title')

		if args.all:
			for i in items:
				fm.print(i)
				open_url(i)
		else:
			selected = term.select([fm.format(i) for i in items])
			for i in [i for s, i in zip(selected, items) if s]:
				open_url(i)

	parser.set_defaults(handler=subcommand)
