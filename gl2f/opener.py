import webbrowser
from . import ls
import argparse
import os
from .ls import board
from .util import terminal as term


def open_url(i):
	url = os.path.join(board.from_id(i['boardId']), i['contentId'])
	webbrowser.open(url, new=0, autoraise=True)

def make_opener(f):
	def g(args):
		items = list(f(args))
		fm = ls.pretty.Formatter(f='date-p:author:title', sep=' ', preview=False)
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


def add_args(parser):
	subparsers = parser.add_subparsers()

	parser_blogs = subparsers.add_parser('blogs')
	ls.lister.add_args(parser_blogs)
	parser_blogs.set_defaults(handler=make_opener(ls.main.blogs))

	parser_radio = subparsers.add_parser('radio')
	ls.lister.add_args(parser_radio)
	parser_radio.set_defaults(handler=make_opener(ls.main.radio))

	parser_news = subparsers.add_parser('news')
	ls.lister.add_args(parser_news)
	parser_news.set_defaults(handler=make_opener(ls.main.news))


	parser.add_argument('-a', '--all', action='store_true',
		help='open all items')