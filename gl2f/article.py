import re
from . import terminal as term

ptn_paragraph = re.compile(r'(?<=<p>).*?(?=</p>)')
ptn_empty_paragraph = re.compile(r'<p></p>')
ptn_media = re.compile(r'<fns-media.*?</fns-media>')
ptn_media_type = re.compile(r'(?<=type=").*?(?=")')
ptn_break = re.compile(r'<br>')

def paragraphs(body):
	return ptn_paragraph.findall(ptn_empty_paragraph.sub('', body))


def compose_full(p):
	if ptn_media.match(p):
		t = '[{}]'.format(ptn_media_type.search(p).group(0))
		return term.mod(t, [term.bold(), term.dim()])
	else:
		return ptn_break.sub('', p)


def to_text(body, opt):
	if opt == 'full':
		return '\n'.join(map(compose_full, paragraphs(body)))


def face(n):
	return '\n{0}・_・{0}\n'.format('-'*n)

