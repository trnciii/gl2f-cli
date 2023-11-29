from .core import lister, pretty, article
from .ayame import terminal as term

def cat(i, args):
	fm = pretty.Formatter()
	fm.print(i, encoding=args.encoding)
	for s in article.lines(i, args.style, args.sixel, args.max_size):
		term.write_with_encoding(s, encoding=args.encoding, errors='ignore')
	term.write_with_encoding('\n', encoding=args.encoding)


def subcommand(args):
	args.max_size = (args.width, args.height) if (args.width or args.height) else None

	if args.board.startswith('https'):
		cat(lister.fetch_content(args.board, dump=args.dump), args)
		return

	items = lister.list_contents(args)

	if args.all:
		for i in items:
			cat(i, args)
	elif args.pick:
		for i in (items[i-1] for i in args.pick if 0<i<=len(items)):
			cat(i, args)
	else:
		fm = pretty.from_args(args, items)
		for i in term.selected(items, fm.format):
			cat(i, args)

def add_to():
	return 'gl2f', 'cat'

def add_args(parser):
	parser.description = 'Display articles'

	lister.add_args(parser)
	pretty.add_args(parser)
	parser.set_defaults(format='author:title')

	parser.add_argument('--encoding')

	parser.add_argument('--style', type=str, choices={'full', 'compact', 'compressed', 'plain'}, default='compact',
		help='Choose style to display articles')
	parser.add_argument('--no-image', dest='sixel', action='store_false',
		help='Do not use sixel image')
	parser.add_argument('-a', '--all', action='store_true',
		help='Show all items')
	parser.add_argument('--pick', type=int, nargs='+',
		help='Select articles to show')
	parser.add_argument('-W', '--width', type=int,
		help='Set max image width')
	parser.add_argument('-H', '--height', type=int,
		help='Set max image height')

	parser.set_defaults(handler=subcommand)


def set_compreply():
	return '__gl2f_complete_list_args'
