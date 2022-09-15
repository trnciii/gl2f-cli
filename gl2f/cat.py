from .core import lister, pretty, article

def name(): return 'cat'

def cat(i, args):
	from .dl import save
	import time

	if args.dl:
		save(i, args)
	fm = pretty.Formatter(f=args.format, fd=args.date, sep=args.sep)
	fm.print(i)
	t0 = time.time()
	text, mediarep = article.to_text(i, args.option)
	t1 = time.time()
	print(text)
	t2 = time.time()
	print('time')
	print('cat', 'to_text', t1-t0, 'print', t2-t1)
	print('sixel', *mediarep.time, sep='\n')
	print('sixel total', 'open', sum(i['open'] for i in mediarep.time), 'sixelize', sum(i['sixelize'] for i in mediarep.time))


def add_args(parser, board):
	lister.add_args(parser)
	pretty.add_args(parser)
	parser.add_argument('--option', type=str, choices=article.to_text_options(), default='compact')
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
			fm_list = pretty.Formatter(f='date-p:author:title', sep=' ')
			selected = term.select([fm_list.format(i) for i in items])
			for i in [i for s, i in zip(selected, items) if s]:
				cat(i, args)

	parser.set_defaults(handler=subcommand)
