from datetime import datetime

def to_datetime(t):
	return datetime.fromtimestamp(t/1000)

def is_today(t):
	return to_datetime(t).date() == datetime.today().date()


def justzen(s, w):
	if w>len(s):
		return s + '　'*(w-len(s))
	else:
		return s