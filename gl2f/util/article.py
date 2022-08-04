import re
from . import terminal as term

ptn_paragraph = re.compile(r'<p>(.*?)</p>')
ptn_media = re.compile(r'<fns-media.*?type="(.+?)".*?></fns-media>')
ptn_break = re.compile(r'<br>')
ptn_link = re.compile(r'<a href="(.+?)".*?>.+?</a>')
ptn_strong = re.compile(r'<strong>(.*?)</strong>')
ptn_span = re.compile(r'<span.*?>(.*?)</span>')


def paragraphs(body):
	return [ptn_paragraph.sub(r'\1', line) for line in ptn_paragraph.findall(body)]


def compose_line(p):
	p = ptn_media.sub(term.mod(r'[\1]', [term.bold(), term.dim()]), p)
	p = ptn_strong.sub(term.mod(r'\1', [term.blink()]), p)
	p = ptn_link.sub(term.mod(r'\1', [term.dim()]), p)
	p = ptn_span.sub('', p)
	p = ptn_break.sub('', p)
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
