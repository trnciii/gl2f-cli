import re, html
from gl2f.util import terminal as term

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


def extract_media(item):
	import requests, urllib.request
	from gl2f import auth

	for media_id, _ in ptn_media.findall(item['values']['body']):

		response = requests.get(
			f"https://api.fensi.plus/v1/sites/girls2-fc/boards/{item['boardId']}/contents/{item['contentId']}/medias/{media_id}",
			headers={
				'origin': 'https://girls2-fc.jp',
				'x-authorization': auth.update(auth.load()),
				'x-from': 'https://girls2-fc.jp',
			})

		if response.ok:
			data = response.json()
			url = data['accessUrl']
			filename = f"{media_id}.{data['meta']['ext']}"
			urllib.request.urlretrieve(url, filename)
