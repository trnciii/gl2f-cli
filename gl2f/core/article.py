import re, html
import argparse
from . import terminal as term, sixel


ptn_paragraph = re.compile(r'<p.*?>(.*?)</p>')
ptn_media = re.compile(r'<fns-media.*?media-id="(.+?)".*?type="(.+?)".*?></fns-media>')
ptn_break = re.compile(r'<br>')
ptn_link = re.compile(r'<a href="(.+?)".*?>.+?</a>')
ptn_strong = re.compile(r'<strong.*?>(.*?)</strong>')
ptn_span = re.compile(r'<span.*?>(.*?)</span>')
ptn_http = re.compile(r'(https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*))')


def paragraphs(body):
	return [ptn_paragraph.sub(r'\1', line) for line in ptn_paragraph.findall(body)]


class MediaRep:
	def __init__(self, item, rep):
		self.boardId = item['boardId']
		self.contentId = item['contentId']

		if rep == 'type':
			self.rep = self.media_rep_type
		elif rep == 'sixel' and sixel.supported():
			self.rep = self.media_rep_sixel
		else:
			self.rep = self.media_rep_type_id


	def media_rep_type(self, p):
		return ptn_media.sub(term.mod('[\\2]', [term.dim()]), p)

	def media_rep_type_id(self, p):
		return ptn_media.sub(term.mod('[\\2](\\1)', [term.dim()]), p)

	def media_rep_sixel(self, p):
		match = ptn_media.search(p)
		if not match:
			return p
		i, t = match.group(1, 2)
		if t != 'image':
			return self.media_rep_type_id(p)

		_, data = dl_medium(self.boardId, self.contentId, i, False, False)
		return sixel.from_bytes(data, (1000, 1000))


def compose_line(p, media_rep):
	p = media_rep.rep(p)
	p = ptn_strong.sub(term.mod('\\1', [term.color('white', 'fl'), term.bold(), term.underline()]), p)
	p = ptn_link.sub(r'\1 ', p)
	p = ptn_span.sub(r'\1', p)
	p = ptn_break.sub('', p)

	# after processing tags
	p = html.unescape(p)
	p = ptn_http.sub(term.mod(r' \1 ', [term.color('blue', 'fl')]), p)

	return p


def to_text_options(): return {'full', 'compact', 'compressed'}

def to_text(item, key):
	body = item['values']['body']

	if key == 'full':
		mediarep = MediaRep(item, 'sixel')
		return '{}\n'.format(
			'\n'.join([compose_line(p, mediarep) for p in paragraphs(body)])
		)

	elif key == 'compact':
		mediarep = MediaRep(item, 'sixel')
		return '{}\n'.format(re.sub(r'\n+', '\n',
			'\n'.join([compose_line(p, mediarep) for p in paragraphs(body)])
		))

	elif key == 'compressed':
		mediarep = MediaRep(item, 'type')
		return '{}\n'.format(''.join([compose_line(p, mediarep) for p in paragraphs(body)]))



def dl_medium(boardId, contentId, mediaId, skip=False, stream=False):
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
		data['originalUrl'] if ('originalUrl' in data.keys() and not stream)\
		else data['accessUrl']
	)

	if response.ok:
		return data, response.content

	else:
		return 'bad response', None


def save_media(item, out, boardId, contentId,
	skip=False, stream=False, force=False, dump=False
):
	import json
	import os
	from . import path


	li = ptn_media.findall(item['values']['body'])
	l = len(li)
	dig = len(str(l))

	dump_data = []
	for i, (mediaId, _) in enumerate(li):

		ptn = re.compile(mediaId + r'\..+')
		if (not force) and any(map(ptn.search, os.listdir(out))):
			continue

		term.clean_row()
		print(f'\rdownloading media [{"#"*i}{"-"*(l-i)}][{i:{dig}}/{l}] {mediaId}', end='', flush=True)


		info, image = dl_medium(boardId, contentId, mediaId, skip, stream)
		dump_data.append(info)

		if image:
			file = os.path.join(out, f'{info["mediaId"]}.{info["meta"]["ext"]}')
			with open(file, 'wb') as f:
				f.write(image)

	term.clean_row()

	if dump:
		with open(f'media-{contentId}.json', 'w') as f:
			json.dump(dump_data, f, indent=2)