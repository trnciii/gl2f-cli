from datetime import datetime
import re


def paragraphs(body):
	return filter(
		lambda x: x!='',
		(re.sub('<[^>]*>', '', para) for para in body.split('<br>'))
	)


def to_datetime(t):
	return datetime.fromtimestamp(t/1000)

def is_today(t):
	return to_datetime(t).date() == datetime.today().date()
