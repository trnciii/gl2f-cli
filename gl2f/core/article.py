import re, html
from . import terminal as term
import json, os, datetime


ptn_paragraph = re.compile(r'<p.*?>(.*?)</p>')
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
	p = ptn_http.sub(term.mod(r' \1 ', [term.color('blue', 'fl')]), p)

	return p


def to_text_options(): return {'full', 'compact', 'compressed'}

def to_text(item, key):
	body = item['values']['body']

	if key == 'full':
		return '{}\n'.format(
			'\n'.join(map(compose_line, paragraphs(body))).rstrip('\n')
		)

	elif key == 'compact':
		return '{}\n'.format(
			re.sub(r'\n+', '\n', '\n'.join(map(compose_line, paragraphs(body))).rstrip('\n'))
		)

	elif key == 'compressed':
		return '{}\n'.format(
			''.join(map(compose_line, paragraphs(body)))
		)


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
	from threading import Lock
	from concurrent.futures import ThreadPoolExecutor

	li = ptn_media.findall(item['values']['body'])
	bar = term.Bar(len(li))

	def dl(mediaId, lock):
		ptn = re.compile(mediaId + r'\..+')
		if (not force) and any(map(ptn.search, os.listdir(out))):
			return 'skipped'

		info, image = dl_medium(boardId, contentId, mediaId, skip, stream)

		lock.acquire()
		bar.inc()
		term.clean_row()
		print(f'downloading media in {contentId} {bar.bar()} {bar.count()}', end='', flush=True)
		lock.release()

		if image:
			file = os.path.join(out, f'{info["mediaId"]}.{info["meta"]["ext"]}')
			with open(file, 'wb') as f:
				f.write(image)

		return info


	lock = Lock()
	with ThreadPoolExecutor() as executor:
		futures = [executor.submit(dl, i, lock) for i, _ in li]

	if dump:
		now = datetime.datetime.now().strftime('%y%m%d%H%M%S')
		with open(os.path.join(dump, f'media-{contentId}-{now}.json'), 'w') as f:
			json.dump([f.result() for f in futures], f, indent=2)


def media_stat(body):
	types = [t for _, t in  ptn_media.findall(body)]
	return {key: types.count(key) for key in ['image', 'video']}
