import re
from . import terminal as term

ptn_paragraph = re.compile(r'(?<=<p>).*?(?=</p>)')
ptn_empty_paragraph = re.compile(r'<p></p>')
ptn_media = re.compile(r'<fns-media.*?</fns-media>')
ptn_media_type = re.compile(r'(?<=type=").*?(?=")')
ptn_break = re.compile(r'<br>')

def paragraphs(body):
	return ptn_paragraph.findall(ptn_empty_paragraph.sub('', body))


def compose_line(p):
	if ptn_media.match(p):
		t = '[{}]'.format(ptn_media_type.search(p).group(0))
		return term.mod(t, [term.bold(), term.dim()])
	else:
		return ptn_break.sub('', p)


to_text_option = {'full', 'compact', 'compressed'}

def to_text(body, key):
	assert key in to_text_option

	if key == 'full':
		return '\n'.join(map(compose_line, paragraphs(body))).rstrip('\n')

	elif key == 'compact':
		text = '\n'.join(map(compose_line, paragraphs(body))).rstrip('\n')
		return re.sub(r'\n+', '\n', text)

	elif key == 'compressed':
		return ''.join(map(compose_line, paragraphs(body)))
