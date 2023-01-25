import re, html
from . import local
from ..ayame import sixel, terminal as term
import json, os, datetime
from .. import auth


ptn_paragraph = re.compile(r'<p.*?>(.*?)</p>')
ptn_media = re.compile(r'<fns-media.*?media-id="(.+?)".*?type="(.+?)".*?></fns-media>')
ptn_break = re.compile(r'<br>')
ptn_link = re.compile(r'<a href="(.+?)".*?>.+?</a>')
ptn_strong = re.compile(r'<strong.*?>(.*?)</strong>')
ptn_span = re.compile(r'<span.*?>(.*?)</span>')
ptn_http = re.compile(r'(https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*))')


class MediaRep:
	def __init__(self, style, contentId, boardId):
		if style == 'type':
			self.rep = self.rep_type

		elif style == 'sixel' and sixel.init():
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
			if data.ok:
				with open(os.path.join(local.refdir('cache'), i), 'wb') as f:
					f.write(data.content)
			image = Image.open(BytesIO(data.content))

		image = sixel.limit(image, (1600, 1600))
		ret = sixel.to_sixel(image)
		return ret


def line_kernel(p, mediarep):
	p = mediarep.rep(p)
	p = ptn_strong.sub(term.mod('\\1', term.color('white', 'fl'), term.bold(), term.underline()), p)
	p = ptn_link.sub(r'\1 ', p)
	p = ptn_span.sub(r'\1', p)
	p = ptn_break.sub('', p)

	# after processing tags
	p = html.unescape(p)
	p = ptn_http.sub(term.mod(r' \1 ', term.color('blue', 'fl')), p)

	return p


def lines(item, style, use_sixel):
	from concurrent.futures import ThreadPoolExecutor
	from functools import partial

	f = partial(line_kernel, mediarep=MediaRep({
		'full': 'sixel' if use_sixel else 'type_id',
		'compact': 'sixel' if use_sixel else 'type_id',
		'compressed': 'type',
		'plain': 'none'
	}[style], item['contentId'], item['boardId']))

	with ThreadPoolExecutor(max_workers=5) as e:
		futures = [e.submit(f, p.group(1)) for p in ptn_paragraph.finditer(item['values']['body'])]

		if style == 'full':
			for f in futures:
				yield f'{f.result()}\n'

		elif style == 'compact':
			for f in futures:
				l = f.result()
				if len(l):
					yield f'{l}\n'

		elif style == 'compressed':
			for f in futures:
				l = f.result()
				if len(l):
					yield f'{l} '
			yield '\n'

		elif style == 'plain':
			for f in futures:
				yield f.result()


def dl_medium(boardId, contentId, mediaId, head=False, stream=False, streamfile=False, xauth=None):
	import requests

	class bad_response:
		ok = False

	response = requests.get(
		f'https://api.fensi.plus/v1/sites/girls2-fc/boards/{boardId}/contents/{contentId}/medias/{mediaId}',
		headers={
			'origin': 'https://girls2-fc.jp',
			'x-authorization': xauth if xauth else auth.update(auth.load()),
			'x-from': 'https://girls2-fc.jp',
		})

	if not response.ok:
		return response, bad_response

	meta = response.json()
	url = meta['accessUrl'] if streamfile else meta.get('originalUrl', meta['accessUrl'])

	if head:
		return meta, requests.head(url)
	else:
		return meta, requests.get(url, stream=stream)


class Bar:
	def __init__(self, li, contentId):
		from threading import Lock

		self.n = len(li)
		self.dig = len(str(self.n))

		w, _ = os.get_terminal_size()
		self.width = w - 2*self.dig - 26

		self.lock = Lock()

		self.contentId = contentId

		self.progress = {k:{'progress':0, 'length':1} for k in li}


	def bar(self):
		f = sum(p['progress']/p['length'] for p in self.progress.values()) / len(self.progress)
		i = int(f*self.width)
		return f'[{"#"*i}{"-"*(self.width-i)}]'

	def count(self):
		i = sum(1 for _ in (i['progress'] for i in self.progress.values() if i['progress']>0))
		return f'[{i:{self.dig}}/{self.n:{self.dig}}]'

	def print(self):
		with self.lock:
			term.clean_row()
			print(f'{self.contentId} {self.bar()} {self.count()}', end='', flush=True)


def save_media(item, out, boardId, contentId,
	skip=False, streamfile=False, force=False, dump=False
):
	from concurrent.futures import ThreadPoolExecutor
	from functools import partial

	li = [i.group(1) for i in ptn_media.finditer(item['values']['body'])]

	bar = Bar(li, contentId)
	bar.print()

	xauth = auth.update(auth.load())
	_dl = partial(dl_medium, boardId, contentId, head=skip, stream=True, streamfile=streamfile, xauth=xauth)

	def dl(mediaId):
		ptn = re.compile(mediaId + r'\..+')
		if (not force) and any(map(ptn.search, os.listdir(out))):
			return 'skipped'

		meta, response = _dl(mediaId=mediaId)

		bar.progress[mediaId]['length'] = int(response.headers['content-length'])

		with open(os.path.join(out, f'{meta["mediaId"]}.{meta["meta"]["ext"]}'), 'wb') as f:
			for i in response.iter_content(chunk_size=1024*1024):
				f.write(i)

				bar.progress[mediaId]['progress'] += len(i)
				bar.print()


		response.close()

		return meta


	with ThreadPoolExecutor() as executor:
		futures = [executor.submit(dl, i) for i in li]

	if dump:
		now = datetime.datetime.now().strftime('%y%m%d%H%M%S')
		with open(os.path.join(dump, f'media-{contentId}-{now}.json'), 'w', encoding='utf-8') as f:
			json.dump([f.result() for f in futures], f, indent=2, ensure_ascii=False)


def media_stat(body):
	types = [t for _, t in  ptn_media.findall(body)]
	return {key: types.count(key) for key in ['image', 'video']}
