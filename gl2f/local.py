import re
import os, json
from .core import pretty, local


def ls(args):
	pretty.post_argparse(args)

	items = [local.load_content(i) for i in local.listdir('contents')]
	if args.order:
		a = args.order.split(':')
		items.sort(key=lambda i: i[a[0]], reverse=(len(a)==2 and a[1]=='desc'))

	fm = pretty.Formatter(f=args.format, fd=args.date, sep=args.sep)
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


def index():
	out = os.path.join(local.home(), 'index.html')
	with open(out, 'w', encoding='utf-8') as f:
		print('<body>', file=f)

		print('<table>', file=f)
		print('<tr><th>Title</th><tr>', file=f)
		for i in local.listdir('contents'):
			item = local.load_content(i)
			print(f'<tr><td><a href=contents/{item["contentId"]}>{item["values"]["title"]}</a></td><tr>', file=f)
		print('</table>', file=f)

		print('</body>', file=f)

	print(f'saved {out}')


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

	p = sub.add_parser('ls')
	p.add_argument('--order', type=str,
		help='sort order')
	pretty.add_args(p)
	p.set_defaults(handler=ls, format='date-p:author:title')

	sub.add_parser('stat').set_defaults(handler=lambda _:stat())