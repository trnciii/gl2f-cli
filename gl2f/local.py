import re
import os, json
from .core import pretty, local


def ls(args):
	items = [local.load_content(i) for i in local.listdir('contents')]
	if args.order:
		a = args.order.split(':')
		items.sort(key=lambda i: i[a[0]], reverse=(len(a)==2 and a[1]=='desc'))

	if not 'page' in args.format:
		args.format = 'page:' + args.format

	fm = pretty.from_args(args, items)
	for i in items:
		fm.print(i, encoding=args.encoding)


def clear_cache():
	if d:=local.refdir_untouch('cache'):
		for i in os.listdir(d):
			os.remove(os.path.join(d, i))

def stat():
	for _par in ['contents', 'cache']:
		if par:=local.refdir_untouch(_par):
			size = sum(sum( os.path.getsize(os.path.join(p,_f)) for _f in f ) for p,_,f in os.walk(par))
			print(f'{_par+"/":10} items: {len(os.listdir(par))} size: {size/(1024**3):,.2f} GB')


def install():
	import shutil

	file = 'site'
	src = local.package_data(file)
	dst = os.path.join(local.home(), file)

	if os.path.exists(dst):
		print(f'reinstalling {dst} that already exits')
		rm = shutil.rmtree if os.path.isdir(dst) else os.remove
		rm(dst)

	cp = shutil.copytree if os.path.isdir(src) else shutil.copyfile
	cp(src, dst)
	print(f'copied site into {dst}')

	index.main()


class index:
	@staticmethod
	def load():
		try:
			path = os.path.join(local.refdir_untouch('site'), 'index.js')
			with open(path, encoding='utf-8') as f:
				raw = f.read()
			return json.loads(re.sub(r'^.+?=', '', raw))

		except:
			return {}


	@staticmethod
	def value(i):
		from .core import board, article

		item = local.load_content(i)
		media = [i for i, _ in article.ptn_media.findall(item['values']['body'])]
		return {
			'title': item['values']['title'],
			'board': board.get('id', item['boardId'])['page'],
			'author': item.get('category', {'name':''})['name'],
			'date': item['openingAt'],
			'media': [''.join(x) for x in sorted(
				filter(lambda x:x[0] in media,
					(os.path.splitext(i) for i in local.listdir(os.path.join('contents', i)))
				),
				key=lambda x:media.index(x[0])
			)],
			'expired': item.get('closingAt', None)
		}


	@staticmethod
	def create_table(contents):
		from concurrent.futures import ThreadPoolExecutor
		with ThreadPoolExecutor() as e:
			values = e.map(index.value, contents)
		return {k:v for k, v in zip(contents, values)}


	@staticmethod
	def main(full=False):
		site = local.refdir_untouch('site')
		if not site:
			if 'n' != input('site not found. install now? (Y/n)').lower():
				install()
			return


		if full:
			table = index.create_table(local.listdir('contents'))
		else:
			prev = index.load()
			contents = list(set(local.listdir('contents')).difference(prev.keys()))
			table = prev | index.create_table(contents)

		out = os.path.join(site, 'index.js')
		with open(out, 'w', encoding='utf-8') as f:
			print(f'const table={json.dumps(table, separators=(",", ":"), ensure_ascii=False)}', file=f)

		print(f'saved {out}')


def open_site():
	import webbrowser

	html = os.path.join(local.home(), 'site', 'index.html')

	if not os.path.exists(html):
		if 'n' != input('could not find site. install now? (Y/n)').lower():
			install()
		else:
			return

	index.main()
	webbrowser.open(f'file://{html}')


def create_html(item):
	from .core import article

	i = item['contentId']
	body = item['values']['body']
	contents = local.refdir_untouch('contents')
	li = local.listdir(f'contents/{i}')

	def up(match):
		m, t = match.groups()
		try:
			p = next(p for p in li if p.startswith(m))
		except:
			return ''

		if t == 'image':
			return f'<img src={contents}/{i}/{p} width=100%></img>'
		elif t == 'video':
			return f'<video controls autoplay muted loop src={contents}/{i}/{p} width=100%></video>'
		else:
			return ''

	return article.ptn_media.sub(up, body)


def build(i, view=False):
	page = os.path.join(local.refdir('site/pages'), f'{i}.html')
	body = create_html(local.load_content(i))
	with open(page, 'w', encoding='utf-8') as f:
		f.write(body)

	print(f'saved file:///{page}')


def add_args(parser):
	sub = parser.add_subparsers()

	p = sub.add_parser('build')
	p.add_argument('content_id')
	p.add_argument('--view', action='store_true')
	p.set_defaults(handler=lambda args: build(args.content_id, args.view))

	sub.add_parser('clear-cache').set_defaults(handler=lambda _:clear_cache())
	sub.add_parser('dir').set_defaults(handler=lambda _:print(local.home()))
	sub.add_parser('index').set_defaults(handler = lambda _:index.main(full=True))
	sub.add_parser('install').set_defaults(handler=lambda _:install())

	p = sub.add_parser('ls')
	p.add_argument('--order', type=str,
		help='sort order')
	pretty.add_args(p)
	p.add_argument('--encoding')
	p.set_defaults(handler=ls, format='author:title')

	sub.add_parser('stat').set_defaults(handler=lambda _:stat())
	sub.add_parser('open').set_defaults(handler=lambda _:open_site())