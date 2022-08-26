import re
import os, json


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
	}

	for k, v in functions.items():
		args = sys.argv[1:]
		if k in args:
			loc = args.index(k)
			v(*args[loc+1:])
