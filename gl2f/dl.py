import argparse
from .core import lister, pretty, article, terminal as term

def name(): return 'dl'

def add_args(parser, board):
	lister.add_args(parser)
	pretty.add_args(parser)

	parser.add_argument('-a', '--all', action='store_true',
		help='preview all items')

	parser.add_argument('--stream', action='store_true',
		help='save video files as stream')

	parser.add_argument('--skip', action='store_true',
		help='not actually download video files')

	parser.add_argument('--force', action='store_true',
		help='force download to overwrite existing files')

	parser.add_argument('-o', type=str, default='',
		help='output path')


	def subcommand(args):
		pretty.post_argparse(args)

		items = list(lister.listers()[board](args))

		if args.all:
			for i in items:
				article.save_media(i, out=args.o, skip=args.skip, stream=args.stream, force=args.force, dump=args.dump)
		else:
			fm_list = pretty.Formatter(f='date-p:author:title', sep=' ')
			selected = term.select([fm_list.format(i) for i in items])
			for i in [i for s, i in zip(selected, items) if s]:
				article.save_media(i, out=args.o, skip=args.skip, stream=args.stream, force=args.force, dump=args.dump)


	parser.set_defaults(handler=subcommand)
