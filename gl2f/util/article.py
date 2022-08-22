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


def dl_medium(boardId, contentId, mediaId, skip, save_original):
	import requests
	from gl2f import auth

	response = requests.get(
		f'https://api.fensi.plus/v1/sites/girls2-fc/boards/{boardId}/contents/{contentId}/medias/{mediaId}',
		headers={
			'origin': 'https://girls2-fc.jp',
			'x-authorization': auth.update(auth.load()),
			'x-from': 'https://girls2-fc.jp',
		})

	if not response.ok:
		return 'bad response', None

	data = response.json()

	if skip:
		return data, None


	response = requests.get(
		data['originalUrl'] if (save_original and 'originalUrl' in data.keys())\
		else data['accessUrl']
	)

	if response.ok:
		return data, response.content

	else:
		return 'bad response', None


def save_media(item, option, dump=False):
	import json
	import os
	from gl2f.util import path


	boardId = item['boardId']
	contentId = item['contentId']

	save_original = option != 'stream'
	skip = option == 'skip'


	li = ptn_media.findall(item['values']['body'])
	l = len(li)
	dig = len(str(l))

	dump_data = []
	for i, (mediaId, _) in enumerate(li):

		ptn = re.compile(mediaId + r'\..+')
		if any(map(ptn.search, path.ls('media'))):
			continue

		term.clean_row()
		print(f'\rdownloading media [{"#"*i}{"-"*(l-i)}][{i:{dig}}/{l}] {mediaId}', end='', flush=True)


		info, image = dl_medium(boardId, contentId, mediaId, skip, save_original)
		dump_data.append(info)

		file = os.path.join(path.media(), f'{info["mediaId"]}.{info["meta"]["ext"]}')
		with open(file, 'wb') as f:
			f.write(image)

	term.clean_row()

	if dump:
		with open(f'media-{contentId}.json', 'w') as f:
			json.dump(dump_data, f, indent=2)


def add_args(parser):
	parser.add_argument('--dl-media', type=str, nargs='?', const='original', choices=['stream', 'original', 'skip'],
		help='save media')