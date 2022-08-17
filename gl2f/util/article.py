import re, html
from gl2f.util import terminal as term
import argparse


ptn_paragraph = re.compile(r'<p>(.*?)</p>')
ptn_media = re.compile(r'<fns-media.*?media-id="(.+?)".*?type="(.+?)".*?></fns-media>')
ptn_break = re.compile(r'<br>')
ptn_link = re.compile(r'<a href="(.+?)".*?>.+?</a>')
ptn_strong = re.compile(r'<strong.*?>(.*?)</strong>')
ptn_span = re.compile(r'<span.*?>(.*?)</span>')
ptn_http = re.compile(r'(https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*))')


def paragraphs(body):
	return [ptn_paragraph.sub(r'\1', line) for line in ptn_paragraph.findall(body)]


def compose_line(p):
	p = ptn_media.sub(term.mod('[\\2](\\1)', [term.dim()]), p)
	p = ptn_strong.sub(term.mod('\\1', [term.color('white', 'fl'), term.bold(), term.underline()]), p)
	p = ptn_link.sub(r'\1 ', p)
	p = ptn_span.sub(r'\1', p)
	p = ptn_break.sub('', p)

	# after processing tags
	p = html.unescape(p)
	p = ptn_http.sub(term.mod(r'\1', [term.color('blue', 'fl')]), p)

	return p


to_text_option = {'full', 'compact', 'compressed'}

def to_text(body, key):
	if key not in to_text_option:
		key = 'compact'


	if key == 'full':
		return '\n'.join(map(compose_line, paragraphs(body))).rstrip('\n')

	elif key == 'compact':
		text = '\n'.join(map(compose_line, paragraphs(body))).rstrip('\n')
		return re.sub(r'\n+', '\n', text)

	elif key == 'compressed':
		return ''.join(map(compose_line, paragraphs(body)))


def save_media(item, option, dump=False):
	import requests, urllib.request
	from gl2f import auth
	import json
	import os, re
	from gl2f.util import path


	boardId = item['boardId']
	contentId = item['contentId']

	save_original = option != 'stream'
	skip = option == 'skip'


	li = ptn_media.findall(item['values']['body'])
	l = len(li)
	dig = len(str(l))

	def sub(i, media_id):
		ptn = re.compile(media_id + r'\..+')
		if any(map(ptn.search, path.ls('media'))):
			return 'file already exists'

		term.clean_row()
		print(f'\rdownloading media [{"#"*i}{"-"*(l-i)}][{i:{dig}}/{l}] ', end='', flush=True)

		response = requests.get(
			f'https://api.fensi.plus/v1/sites/girls2-fc/boards/{boardId}/contents/{contentId}/medias/{media_id}',
			headers={
				'origin': 'https://girls2-fc.jp',
				'x-authorization': auth.update(auth.load()),
				'x-from': 'https://girls2-fc.jp',
			})

		if not response.ok:
			return 'bad response'

		data = response.json()
		basename = f'{data["mediaId"]}.{data["meta"]["ext"]}'
		file = os.path.join(path.media(), basename)

		print(f'{basename} ', end='', flush=True)

		if not skip:
			urllib.request.urlretrieve(
				data['originalUrl'] if (save_original and 'originalUrl' in data.keys())\
				else data['accessUrl'],
				file
			)

		return data


	result = {media_id: sub(i, media_id) for i, (media_id, _) in enumerate(li)}

	term.clean_row()

	if dump:
		with open(f"media-{item['contentId']}.json", 'w') as f:
			json.dump(result, f, indent=2)


def add_args(parser):
	parser.add_argument('--dl-media', type=str, nargs='?', const='original', choices=['stream', 'original', 'skip'],
		help='save media')