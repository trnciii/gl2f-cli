from .core import lister, pretty, article

def name(): return 'cat'

def cat(i, args):
	from .dl import save
	import time
	from .core import log

	if args.dl:
		save(i, args)
	print()
	fm = pretty.Formatter(f=args.format, fd=args.date, sep=args.sep)
	fm.print(i)
	t0 = time.time()
	text = article.to_text(i, args.style, args.sixel)
	t1 = time.time()
	print(text)
	t2 = time.time()
	log(f'compose {t1-t0}, print {t2-t1}')


def add_args(parser, board):
	lister.add_args(parser)
	pretty.add_args(parser)
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

		pretty.post_argparse(args)

		items = lister.listers()[board](args)

		if args.all:
			for i in items:
				cat(i, args)
		else:
			fm_list = pretty.Formatter(f='date-p:author:title')
			selected = term.select([fm_list.format(i) for i in items])
			for i in [i for s, i in zip(selected, items) if s]:
				cat(i, args)

	parser.set_defaults(handler=subcommand)
