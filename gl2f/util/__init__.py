from . import article, member, terminal


from datetime import datetime

def to_datetime(t):
	return datetime.fromtimestamp(t/1000)

def is_today(t):
	return to_datetime(t).date() == datetime.today().date()
