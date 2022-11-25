import re
import os, json
from .core import pretty, local


def ls(args):
	items = [local.load_content(i) for i in local.listdir('contents')]
	if args.order:
		a = args.order.split(':')
		items.sort(key=lambda i: i[a[0]], reverse=(len(a)==2 and a[1]=='desc'))

	fm = pretty.from_args(args)
	for i in items:
		fm.print(i)


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

	index()


def index():
	from .core import board

	site = local.refdir_untouch('site')
	if not site:
		if 'n' != input('site not found. install now? (Y/n)').lower():
			install()
		return

	def value(i):
		item = local.load_content(i)
		return {
			'title': item['values']['title'],
			'board': board.get('id', item['boardId'])['page'],
			'author': item.get('category', {'name':''})['name'],
			'date': item['openingAt'],
			'media': list(filter(lambda x:not x.endswith('.json'), local.listdir(os.path.join('contents', i))))
		}

	table = {i: value(i) for i in local.listdir('contents')}

	out = os.path.join(site, 'index.js')
	with open(out, 'w', encoding='utf-8') as f:
		print(f'const table={json.dumps(table, separators=(",", ":"), ensure_ascii=False)}', file=f)

	print(f'saved {out}')


def open_site():
	import webbrowser
	html = os.path.join(local.home(), 'site', 'index.html')
	if os.path.exists(html):
		webbrowser.open(f'file://{html}')
	else:
		print('site is not installed')


def extract_bodies(filename):
	with open(filename) as f:
		log = json.load(f)

	dirname = os.path.splitext(filename)[0]
	os.makedirs(dirname, exist_ok=True)

	para = re.compile(r'(?P<all><p>.*?</p>)')
	breaks = re.compile(r'\n+')

	for i, item in enumerate(log['list']):
		title = re.sub('/', r'-', item['values']['title'])
		body = breaks.sub('\n', para.sub(r'\n\g<all>\n', item['values']['body']))
		base = f'{i}-{title}.html'
		with open(os.path.join(dirname, base), 'w', encoding='utf-8') as f:
			f.write(body)


def add_args(parser):
	sub = parser.add_subparsers()

	sub.add_parser('clear-cache').set_defaults(handler=lambda _:clear_cache())
	sub.add_parser('dir').set_defaults(handler=lambda _:print(local.home()))
	sub.add_parser('index').set_defaults(handler=lambda _:index())
	sub.add_parser('install').set_defaults(handler=lambda _:install())

	p = sub.add_parser('ls')
	p.add_argument('--order', type=str,
		help='sort order')
	pretty.add_args(p)
	p.set_defaults(handler=ls, format='author:title')

	sub.add_parser('stat').set_defaults(handler=lambda _:stat())
	sub.add_parser('open').set_defaults(handler=lambda _:open_site())