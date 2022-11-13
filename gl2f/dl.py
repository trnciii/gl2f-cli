from .core import lister, pretty

def name(): return 'dl'

def save(item, args):
	import json, os
	from .core import local, article, terminal as term

	boardId = item['boardId']
	contentId = item['contentId']

	if args.o:
		out = os.path.join(args.o, contentId)
		os.makedirs(out, exist_ok=True)
	else:
		out = local.refdir(os.path.join('contents', contentId))

	with open(os.path.join(out, f'{contentId}.json'), 'w') as f:
		f.write(json.dumps(item, indent=2))

	article.save_media(item, out, boardId, contentId,
		skip=args.skip, stream=args.stream, force=args.force, dump=args.dump)

	term.clean_row()
	fm = pretty.Formatter(f='id:media:author:title')
	print('downloaded', fm.format(item))


def add_args(parser, list_board):
	lister.add_args(parser)

	pretty.add_args(parser)
	parser.set_defaults(format='author:media:title')

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
		from .core import terminal as term
		from .core.local import refdir_untouch
		from .local import index

		items = list_board(args)

		if args.all:
			for i in items:
				save(i, args)
		else:
			fm = pretty.from_args(args)
			selected = term.select([fm.format(i) for i in items])
			for i in [i for s, i in zip(selected, items) if s]:
				save(i, args)

		if refdir_untouch('site'):
			index()

	parser.set_defaults(handler=subcommand)
