from .core import lister, pretty, article

def name(): return 'cat'

def cat(i, args):
	from .dl import save

	if args.dl:
		save(i, args)
	print()
	fm = pretty.Formatter()
	fm.print(i)
	print(article.to_text(i, args.style, args.sixel))


def add_args(parser, list_board):
	lister.add_args(parser)
	pretty.add_args(parser)
	parser.set_defaults(format='author:title')

	parser.add_argument('--style', type=str, choices=article.style_options(), default='compact')
	parser.add_argument('--no-image', dest='sixel', action='store_false',
		help='not use sixel image')
	parser.add_argument('-a', '--all', action='store_true',
		help='preview all items')
	parser.add_argument('--dl', action='store_true',
		help='also downloads the article')

	# options from dl
	parser.add_argument('--stream', action='store_true',
		help='save video files as stream')
	parser.add_argument('--skip', action='store_true',
		help='not actually download video files')
	parser.add_argument('--force', action='store_true',
		help='force download to overwrite existing files')
	parser.add_argument('-o', type=str, default='',
		help='output path')


	def subcommand(args):
		from .core import terminal as term

		items = list_board(args)

		if args.all:
			for i in items:
				cat(i, args)
		else:
			fm = pretty.from_args(args)
			selected = term.select([fm.format(i) for i in items])
			for i in [i for s, i in zip(selected, items) if s]:
				cat(i, args)

	parser.set_defaults(handler=subcommand)
