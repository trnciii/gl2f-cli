from .core import lister

def name(): return 'dl'

def save(item, args):
	import json, os
	from .core import path, article, terminal as term, pretty

	boardId = item['boardId']
	contentId = item['contentId']

	if args.o:
		out = os.path.join(args.o, contentId)
		os.makedirs(out, exist_ok=True)
	else:
		out = path.refdir(os.path.join('contents', contentId))

	with open(os.path.join(out, f'{contentId}.json'), 'w') as f:
		f.write(json.dumps(item, indent=2))

	article.save_media(item, out, boardId, contentId,
		skip=args.skip, stream=args.stream, force=args.force, dump=args.dump)

	term.clean_row()
	fm = pretty.Formatter(f='id:author:title')
	print('downloaded', fm.format(item))


def add_args(parser, board):
	lister.add_args(parser)

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
		from .core import terminal as term, pretty

		items = lister.listers()[board](args)

		if args.all:
			for i in items:
				save(i, args)
		else:
			fm_list = pretty.Formatter(f='date-p:author:media:title')
			selected = term.select([fm_list.format(i) for i in items])
			for i in [i for s, i in zip(selected, items) if s]:
				save(i, args)


	parser.set_defaults(handler=subcommand)
