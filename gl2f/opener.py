import webbrowser
import argparse
import os
from .core import board, lister, pretty, terminal as term

def name(): return 'open'

def open_url(i):
	url = os.path.join(board.from_id(i['boardId']), i['contentId'])
	webbrowser.open(url, new=0, autoraise=True)

def make_opener(f):
	def g(args):
		items = list(f(args))
		fm = pretty.Formatter(f='date-p:author:title', sep=' ')
		fm.reset_index(digits=len(str(args.number)))

		if args.all:
			for i in items:
				fm.print(i)
				open_url(i)
		else:
			selected = term.select([fm.format(i) for i in items])
			for i in [i for s, i in zip(selected, items) if s]:
				open_url(i)

	return g


def add_args(parser, board):
	lister.add_args(parser)
	parser.add_argument('-a', '--all', action='store_true',
		help='open all items')


	def subcommand(args):
		items = list(lister.listers()[board](args))
		fm = pretty.Formatter(f='date-p:author:title', sep=' ')

		if args.all:
			for i in items:
				fm.print(i)
				open_url(i)
		else:
			selected = term.select([fm.format(i) for i in items])
			for i in [i for s, i in zip(selected, items) if s]:
				open_url(i)

	parser.set_defaults(handler=subcommand)
