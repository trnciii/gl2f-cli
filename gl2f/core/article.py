import re, html
from . import terminal as term, sixel, local
import json, os, datetime
from .. import auth


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
	def __init__(self, style, contentId, boardId):
		if style == 'type':
			self.rep = self.rep_type

		elif style == 'sixel' and sixel.supported():
			from functools import partial

			local.refdir('cache')
			self.contentId = contentId
			self.dl = partial(dl_medium, boardId, self.contentId, xauth=auth.update(auth.load()))
			self.rep = self.rep_sixel

		elif style == 'none':
			self.rep = self.rep_none

		else:
			self.rep = self.rep_type_id

	def rep_none(self, p):
		return ptn_media.sub('', p)

	def rep_type(self, p):
		return ptn_media.sub(term.mod('[\\2]', term.dim()), p)

	def rep_type_id(self, p):
		return ptn_media.sub(term.mod('[\\2](\\1)', term.dim()), p)

	def rep_sixel(self, p):
		from io import BytesIO
		from PIL import Image
		import time

		match = ptn_media.search(p)
		if not match:
			return p
		i, t = match.group(1, 2)
		if t != 'image':
			return self.rep_type_id(p)

		if file:=local.search_media(i, self.contentId):
			image = Image.open(file)
		else:
			_, data = self.dl(mediaId=i)
			if data:
				with open(os.path.join(local.refdir('cache'), i), 'wb') as f:
					f.write(data)
			image = Image.open(BytesIO(data))

		image = sixel.limit(image, (1000, 1000))
		ret = sixel.to_sixel(image)
		return ret


def compose_line(p, mediarep):
	p = mediarep.rep(p)
	p = ptn_strong.sub(term.mod('\\1', term.color('white', 'fl'), term.bold(), term.underline()), p)
	p = ptn_link.sub(r'\1 ', p)
	p = ptn_span.sub(r'\1', p)
	p = ptn_break.sub('', p)

	# after processing tags
	p = html.unescape(p)
	p = ptn_http.sub(term.mod(r' \1 ', term.color('blue', 'fl')), p)

	return p


def lines(item, mediarepstyle):
	from concurrent.futures import ThreadPoolExecutor

	body = item['values']['body']
	m = MediaRep(mediarepstyle, item['contentId'], item['boardId'])

	with ThreadPoolExecutor() as executor:
		futures = [executor.submit(compose_line, p, m) for p in paragraphs(body)]
	return [f.result() for f in futures]


def style_options(): return {'full', 'compact', 'compressed', 'plain'}

def to_text(item, key, use_sixel=True):
	if key == 'full':
		return '\n'.join(lines(item, 'sixel' if use_sixel else 'type_id'))

	elif key == 'compact':
		return '\n'.join(filter(len, lines(item, 'sixel' if use_sixel else 'type_id')))

	elif key == 'compressed':
		return ' '.join(filter( len, lines(item, 'type') ))

	elif key == 'plain':
		return ''.join(lines(item, 'none'))



def dl_medium(boardId, contentId, mediaId, skip=False, stream=False, xauth=None):
	import requests

	response = requests.get(
		f'https://api.fensi.plus/v1/sites/girls2-fc/boards/{boardId}/contents/{contentId}/medias/{mediaId}',
		headers={
			'origin': 'https://girls2-fc.jp',
			'x-authorization': xauth if xauth else auth.update(auth.load()),
			'x-from': 'https://girls2-fc.jp',
		})

	if not response.ok:
		return {'error': 'bad response at url query', 'reason': response.reason}, None

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
		return {'error': 'bad response at media download', 'reason': response.reason}, None


def save_media(item, out, boardId, contentId,
	skip=False, stream=False, force=False, dump=False
):
	from threading import Lock
	from concurrent.futures import ThreadPoolExecutor

	li = ptn_media.findall(item['values']['body'])
	bar = term.Bar(len(li))
	lock = Lock()
	xauth = auth.update(auth.load())

	def dl(mediaId):
		ptn = re.compile(mediaId + r'\..+')
		if (not force) and any(map(ptn.search, os.listdir(out))):
			return 'skipped'

		info, image = dl_medium(boardId, contentId, mediaId, skip, stream, xauth=xauth)

		with lock:
			bar.inc()
			term.clean_row()
			print(f'downloading media in {contentId} {bar.bar()} {bar.count()}', end='', flush=True)

		if image:
			file = os.path.join(out, f'{info["mediaId"]}.{info["meta"]["ext"]}')
			with open(file, 'wb') as f:
				f.write(image)

		return info


	with ThreadPoolExecutor() as executor:
		futures = [executor.submit(dl, i) for i, _ in li]

	if dump:
		now = datetime.datetime.now().strftime('%y%m%d%H%M%S')
		with open(os.path.join(dump, f'media-{contentId}-{now}.json'), 'w', encoding='utf-8') as f:
			json.dump([f.result() for f in futures], f, indent=2, ensure_ascii=False)


def media_stat(body):
	types = [t for _, t in  ptn_media.findall(body)]
	return {key: types.count(key) for key in ['image', 'video']}
