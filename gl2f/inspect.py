import re
import os, json
from gl2f.core import path


def load_content(i):
	with open(os.path.join(path.ref('contents'), i, f'{i}.json')) as f:
		return json.load(f)

def ls(key=None):
	from gl2f.core import pretty

	items = [load_content(i) for i in os.listdir(path.ref('contents'))]
	if key:
		items.sort(key=key)

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


if __name__ == '__main__':
	import sys

	functions = {
		'body': extract_bodies,
		'ls': lambda:ls(key=lambda i:i['openingAt'])
	}

	for k, v in functions.items():
		args = sys.argv[1:]
		if k in args:
			loc = args.index(k)
			v(*args[loc+1:])
