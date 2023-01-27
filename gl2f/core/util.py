from datetime import datetime

def to_datetime(t):
	return datetime.fromtimestamp(t/1000)
