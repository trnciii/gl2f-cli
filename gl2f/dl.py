import argparse
from .core import lister, pretty, article, terminal as term

def name(): return 'dl'

def add_args(parser, board):
	lister.add_args(parser)
	pretty.add_args(parser)
	parser.add_argument('--option', type=str, choices=article.save_media_options(), default='original')
	parser.add_argument('-a', '--all', action='store_true',
		help='preview all items')


	def subcommand(args):
		pretty.post_argparse(args)

		items = list(lister.listers()[board](args))

		if args.all:
			for i in items:
				article.save_media(i, option=args.option, dump=args.dump_response)
		else:
			fm_list = pretty.Formatter(f='date-p:author:title', sep=' ')
			selected = term.select([fm_list.format(i) for i in items])
			for i in [i for s, i in zip(selected, items) if s]:
				article.save_media(i, option=args.option, dump=args.dump_response)


	parser.set_defaults(handler=subcommand)
