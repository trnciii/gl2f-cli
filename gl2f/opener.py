import webbrowser
from . import ls
import argparse
import os
from .ls import board


def make_opener(f):
	def g(args):
		items = list(f(args))
		fm = ls.pretty.Formatter(f='date-p:author:title', sep=' ', preview=False)
		fm.reset_index(digits=len(str(args.number)))

		for i in items:
			fm.print(i)

		if 'n' == input('Opening all above. (Y/n)').lower():
			return

		for i in items:
			url = os.path.join(board.from_id(i['boardId']), i['contentId'])
			webbrowser.open(url, new=0, autoraise=True)

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
