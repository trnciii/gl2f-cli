import re
import os, json
from gl2f.core import path


def load_content(i):
	with open(os.path.join(path.refdir('contents'), i, f'{i}.json')) as f:
		return json.load(f)

def ls(args):
	from gl2f.core import pretty

	items = [load_content(i) for i in os.listdir(path.refdir('contents'))]
	if args.order:
		a = args.order.split(':')
		items.sort(key=lambda i: i[a[0]], reverse=(len(a)==2 and a[1]=='desc'))

	fm = pretty.Formatter(f='date-p:author:title')
	for i in items:
		fm.print(i)


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

	p = sub.add_parser('ls')
	p.add_argument('--order', type=str,
		help='sort order')
	p.set_defaults(handler=ls)


if __name__ == '__main__':
	import sys

	functions = {
		'body': extract_bodies,
	}

	for k, v in functions.items():
		args = sys.argv[1:]
		if k in args:
			loc = args.index(k)
			v(*args[loc+1:])
