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