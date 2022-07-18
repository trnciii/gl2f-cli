from datetime import datetime
import re


def paragraphs(body):
	lines = [re.sub('<[^>]*>', '', line) for line in body.split('<br>')]
	return filter(lambda x: x!='', lines)


def to_datetime(t):
	return datetime.fromtimestamp(t/1000)

def is_today(t):
	return to_datetime(t).date() == datetime.today().date()


def justzen(s, w):
	if w>len(s):
		return s + '　'*(w-len(s))
	else:
		return s

def term_rgb(r, g, b, bg='f'):
	if bg in ['b', 'bg', 'background']:
		return f'[48;2;{r};{g};{b}'
	else:
		return f'[38;2;{r};{g};{b}'

def term_mod(s, cc):
	default = '\033[0m'
	return ''.join([f'\33{c}m' for c in cc]) + s + default
