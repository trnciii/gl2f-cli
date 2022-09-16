import re, html
import json, os, datetime, asyncio
from . import terminal as term, sixel, path


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

		self.time = []


	def media_rep_type(self, p):
		return ptn_media.sub(term.mod('[\\2]', [term.dim()]), p)

	def media_rep_type_id(self, p):
		return ptn_media.sub(term.mod('[\\2](\\1)', [term.dim()]), p)

	def media_rep_sixel(self, p):
		from io import BytesIO
		from PIL import Image
		import time

		match = ptn_media.search(p)
		if not match:
			return p
		i, t = match.group(1, 2)
		if t != 'image':
			return self.media_rep_type_id(p)

		t0 = time.time()
		if file:=self.search_local(i):
			image = Image.open(file)
			cachehit = True
		else:
			_, data = dl_medium(self.boardId, self.contentId, i, False, False)
			if data:
				with open(os.path.join(path.ref('cache'), i), 'wb') as f:
					f.write(data)
			image = Image.open(BytesIO(data))
			cachehit = False
		t1 = time.time()

		image = sixel.limit(image, (1000, 1000))
		ret = sixel.to_sixel(image)
		t2 = time.time()
		self.time.append({'cache-hit': cachehit, 'open': t1-t0, 'sixelize': t2-t1})
		return ret


	def search_local(self, mediaId):
		cache = path.ref_untouch(f'cache/{mediaId}')
		if os.path.exists(cache):
			return cache

		directory = path.ref_untouch(f'contents/{self.contentId}')
		if not os.path.exists(directory):
			return None

		pattern = re.compile(rf'{mediaId}.*')
		li = filter(pattern.match, os.listdir(directory))

		try:
			return os.path.join(directory, next(li))
		except:
			return None


async def compose_line(p, media_rep):
	loop = asyncio.get_event_loop()

	p = await loop.run_in_executor(None, media_rep.rep, p)
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

	loop = asyncio.get_event_loop()

	def lines(mediarep):
		jobs = [compose_line(p, mediarep) for p in paragraphs(body)]
		return loop.run_until_complete(asyncio.gather(*jobs))

	if key == 'full':
		mediarep = MediaRep(item, 'sixel')
		return '{}\n'.format('\n'.join(lines(mediarep))), mediarep

	elif key == 'compact':
		mediarep = MediaRep(item, 'sixel')
		return '{}\n'.format(re.sub(r'\n+', '\n', '\n'.join(lines(mediarep)))), mediarep

	elif key == 'compressed':
		mediarep = MediaRep(item, 'type')
		return '{}\n'.format(''.join(lines(mediarep))), mediarep



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
	loop = asyncio.get_event_loop()

	li = ptn_media.findall(item['values']['body'])
	bar = term.Bar(len(li))

	async def dl(mediaId):
		ptn = re.compile(mediaId + r'\..+')
		if (not force) and any(map(ptn.search, os.listdir(out))):
			return 'skipped'

		info, image = await loop.run_in_executor(None, dl_medium, boardId, contentId, mediaId, skip, stream)

		bar.inc()
		term.clean_row()
		print(f'downloading media in {contentId} {bar.bar()} {bar.count()}', end='', flush=True)

		if image:
			file = os.path.join(out, f'{info["mediaId"]}.{info["meta"]["ext"]}')
			with open(file, 'wb') as f:
				f.write(image)

		return info


	result = loop.run_until_complete(asyncio.gather(*[dl(i) for i, _ in li]))

	if dump:
		now = datetime.datetime.now().strftime('%y%m%d%H%M%S')
		with open(os.path.join(dump, f'media-{contentId}-{now}.json'), 'w') as f:
			json.dump(result, f, indent=2)


def media_stat(body):
	types = [t for _, t in  ptn_media.findall(body)]
	return {key: types.count(key) for key in ['image', 'video']}
