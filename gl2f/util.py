import datetime

def to_datetime(t):
	return datetime.datetime.fromtimestamp(t/1000)


def justzen(s, w):
	if w>len(s):
		return s + '　'*(w-len(s))
	else:
		return s