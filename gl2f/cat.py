import argparse
from .core import lister, pretty, article, terminal as term

def name(): return 'cat'

def cat(i, args):
	fm = pretty.Formatter(f=args.format, fd=args.date_format, sep=args.sep)
	fm.print(i)
	print(article.to_text(i, args.option))


def add_args(parser, board):
	lister.add_args(parser)
	pretty.add_args(parser)
	parser.add_argument('--option', type=str, choices=article.to_text_options(), default='compact')
	parser.add_argument('-a', '--all', action='store_true',
		help='preview all items')


	def subcommand(args):
		pretty.post_argparse(args)

		items = list(lister.listers()[board](args))

		if args.all:
			for i in items:
				cat(i, args)
		else:
			fm_list = pretty.Formatter(f='date-p:author:title', sep=' ')
			selected = term.select([fm_list.format(i) for i in items])
			for i in [i for s, i in zip(selected, items) if s]:
				cat(i, args)

	parser.set_defaults(handler=subcommand)
