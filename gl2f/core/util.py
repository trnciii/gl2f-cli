from datetime import datetime

def to_datetime(t):
	return datetime.fromtimestamp(t/1000)

def in24h(t):
	diff = datetime.now() - to_datetime(t)
	return diff.total_seconds() < 24*3600
