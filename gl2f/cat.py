from .core import lister, pretty, article, util
from .ayame import terminal as term, sixel

def gen(items, args):
	fm = pretty.from_args(args)
	for i in items:
		yield fm.format(i)
		yield from article.lines(i, args.style, args.sixel, args.max_size)
		yield ''

def subcommand(args):
	args.max_size = (args.width, args.height) if (args.width or args.height) else None

	never_page = args.scroll == 'never' or (args.sixel and sixel.init())

	if args.board.startswith('https'):
		g = gen([lister.fetch_content(args.board, dump=args.dump)], args)
	elif args.all:
		items, _ = lister.list_contents(args)
		g = gen(items, args)
	elif args.pick:
		items, _ = lister.list_contents(args)
		g = gen(util.pick(items, args.pick), args)
	else:
		g = gen(lister.selected(args, pretty.from_args(args).format), args)

	if never_page:
		for line in g:
			term.write_with_encoding(f'{line}\n', encoding=args.encoding)
	else:
		term.scroll(g, eof=util.rule)

def add_to():
	return 'gl2f', 'cat'

def add_args(parser):
	parser.description = 'Display articles'

	lister.add_args(parser)
	pretty.add_args(parser)
	parser.set_defaults(format='author:title')
	util.add_paging_args(parser, 'never')

	parser.add_argument('--encoding')
	parser.add_argument('--style', type=str, choices={'full', 'compact', 'compressed', 'plain'}, default='compact')
	parser.add_argument('--no-image', dest='sixel', action='store_false',
		help='not use sixel image')
	parser.add_argument('-a', '--all', action='store_true',
		help='preview all items')
	parser.add_argument('--pick', type=int, nargs='+',
		help='select articles to show')
	parser.add_argument('--dl', action='store_true',
		help='also downloads the article')
	parser.add_argument('-W', '--width', type=int,
		help='set max image width')
	parser.add_argument('-H', '--height', type=int,
		help='set max image height')

	parser.set_defaults(handler=subcommand)


def set_compreply():
	return '__gl2f_complete_list_args'
