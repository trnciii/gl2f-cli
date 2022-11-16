from .core import lister, pretty

def name(): return 'open'

def open_url(i):
	import webbrowser
	from .core import board
	webbrowser.open(board.content_url(i), new=0, autoraise=True)


def add_args(parser, list_board):
	lister.add_args(parser)
	pretty.add_args(parser)
	parser.set_defaults(format='author:title')
	parser.add_argument('-a', '--all', action='store_true',
		help='open all items')


	def subcommand(args):
		from .core import terminal as term

		items = list_board(args)
		fm = pretty.from_args(args)

		if args.all:
			for i in items:
				fm.print(i)
				open_url(i)
		else:
			selected = term.select([fm.format(i) for i in items])
			for i in [i for s, i in zip(selected, items) if s]:
				open_url(i)

	parser.set_defaults(handler=subcommand)
