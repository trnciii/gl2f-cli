from .core import lister, pretty
from .ayame import terminal as term
import os

def name(): return 'dl'

class Bar:
	def __init__(self, li, contentId):
		from threading import Lock

		self.n = len(li)
		self.dig = len(str(self.n))

		w, _ = os.get_terminal_size()
		self.width = w - 2*self.dig - 26

		self.lock = Lock()

		self.contentId = contentId

		self.progress = {k:{'progress':0, 'length':1} for k in li}


	def bar(self):
		f = sum(p['progress']/p['length'] for p in self.progress.values()) / len(self.progress)
		i = int(f*self.width)
		return f'[{"#"*i}{"-"*(self.width-i)}]'

	def count(self):
		i = sum(1 for _ in (i['progress'] for i in self.progress.values() if i['progress']>0))
		return f'[{i:{self.dig}}/{self.n:{self.dig}}]'

	def print(self):
		with self.lock:
			term.clean_row()
			print(f'{self.contentId} {self.bar()} {self.count()}', end='', flush=True)


def save(item, args):
	import json, datetime, re
	from .core import local, article, auth
	from concurrent.futures import ThreadPoolExecutor
	from functools import partial

	boardId = item['boardId']
	contentId = item['contentId']

	if args.o:
		out = os.path.join(args.o, contentId)
		os.makedirs(out, exist_ok=True)
	else:
		out = local.refdir(os.path.join('contents', contentId))

	with open(os.path.join(out, f'{contentId}.json'), 'w', encoding='utf-8') as f:
		f.write(json.dumps(item, indent=2, ensure_ascii=False))


	li = [i.group(1) for i in article.ptn_media.finditer(item['values']['body'])]

	bar = Bar(li, contentId)
	bar.print()

	xauth = auth.update(auth.load())
	_dl = partial(article.dl_medium, boardId, contentId,
		head=args.skip, stream=True, streamfile=args.stream, xauth=xauth
	)

	def dl(mediaId):
		ptn = re.compile(mediaId + r'\..+')
		if (not args.force) and any(map(ptn.search, os.listdir(out))):
			return 'skipped'

		meta, response = _dl(mediaId=mediaId)

		bar.progress[mediaId]['length'] = int(response.headers['content-length'])

		with open(os.path.join(out, f'{meta["mediaId"]}.{meta["meta"]["ext"]}'), 'wb') as f:
			for i in response.iter_content(chunk_size=1024*1024):
				f.write(i)

				bar.progress[mediaId]['progress'] += len(i)
				bar.print()

		response.close()

		return meta


	with ThreadPoolExecutor() as executor:
		futures = [executor.submit(dl, i) for i in li]

	if args.dump:
		now = datetime.datetime.now().strftime('%y%m%d%H%M%S')
		with open(os.path.join(args.dump, f'media-{contentId}-{now}.json'), 'w', encoding='utf-8') as f:
			json.dump([f.result() for f in futures], f, indent=2, ensure_ascii=False)


	term.clean_row()
	fm = pretty.Formatter(f='id:media:author:title')
	print('downloaded', fm.format(item))


def subcommand(args):
	from .core.local import refdir_untouch
	from .local import index

	if args.board.startswith('https'):
		save(lister.fetch_content(args.board, dump=args.dump), args)
		return

	items = lister.list_contents(args)

	if args.all:
		for i in items:
			save(i, args)
	elif args.pick:
		for i in (items[i-1] for i in args.pick if 0<i<=len(items)):
			save(i, args)
	else:
		fm = pretty.from_args(args, items)
		selected = term.select([fm.format(i) for i in items])
		for i in [i for s, i in zip(selected, items) if s]:
			save(i, args)

	if refdir_untouch('site'):
		index.main()


def add_args(parser):
	lister.add_args(parser)

	pretty.add_args(parser)
	parser.set_defaults(format='author:media:title')

	parser.add_argument('-a', '--all', action='store_true',
		help='preview all items')

	parser.add_argument('--pick', type=int, nargs='+',
		help='select articles to show')

	parser.add_argument('--stream', action='store_true',
		help='save video files as stream file')

	parser.add_argument('--skip', action='store_true',
		help='not actually download video files')

	parser.add_argument('-F', '--force', action='store_true',
		help='force download to overwrite existing files')

	parser.add_argument('-o', type=str, default='',
		help='output path')

	parser.set_defaults(handler=subcommand)
