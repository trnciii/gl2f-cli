import os
from .core import lister, pretty, article, util
from .ayame import terminal as term, sixel

def cat(i, args):
	from .dl import save

	if args.dl:
		save(i, args)
	fm = pretty.Formatter()
	fm.print(i, encoding=args.encoding)
	for s in article.lines(i, args.style, args.sixel, args.max_size):
		term.write_with_encoding(f'{s}\n', encoding=args.encoding, errors='ignore')
	term.write_with_encoding('\n', encoding=args.encoding)

def gen(items, args, never_page):
	from .dl import save
	fm = pretty.from_args(args)
	for i in items:
		if args.dl:
			save(i, args)

		yield fm.format(i)
		yield from article.lines(i, args.style, args.sixel, args.max_size)
		yield ''

def subcommand(args):
	args.max_size = (args.width, args.height) if (args.width or args.height) else None

	never_page = args.paging == 'never' or (args.sixel and sixel.init())

	if args.board.startswith('https'):
		g = gen([lister.fetch_content(args.board, dump=args.dump)], args, never_page)
	elif args.all:
		items, _ = lister.list_contents(args)
		g = gen(items, args, never_page)
	elif args.pick:
		items, _ = lister.list_contents(args)
		g = gen(util.pick(items, args.pick), args, never_page)
	else:
		g = gen(lister.selected(args, pretty.from_args(args).format), args, never_page)

	if never_page:
		for line in g:
			print(line)
	else:
		term.scroll(g, eof=lambda:util.rule())

def add_to():
	return 'gl2f', 'cat'

def add_args(parser):
	parser.description = 'Display articles'

	lister.add_args(parser)
	pretty.add_args(parser)
	parser.set_defaults(format='author:title')

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
	parser.add_argument('--paging', type=str, choices={'auto', 'never'}, default='auto',
		help='specify when to use the pager, or use `-P` to disable (*auto*, never)')
	parser.add_argument('-P', dest='paging', action='store_const', const='never')

	# options from dl
	parser.add_argument('--stream', action='store_true',
		help='save video files as stream')
	parser.add_argument('--skip', action='store_true',
		help='not actually download video files')
	parser.add_argument('-F', '--force', action='store_true',
		help='force download to overwrite existing files')
	parser.add_argument('-o', type=str, default='',
		help='output path')

	parser.set_defaults(handler=subcommand)


def set_compreply():
	return '__gl2f_complete_list_args'
