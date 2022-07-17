import datetime

def to_datetime(t):
	return datetime.datetime.fromtimestamp(t/1000)
