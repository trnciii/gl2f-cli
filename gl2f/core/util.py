from datetime import datetime
import os, json

def to_datetime(t):
	return datetime.fromtimestamp(t/1000)

def dump(loc, name, data):
	now = datetime.now().strftime('%y%m%d%H%M%S')
	filepath = os.path.join(loc, f'{name}-{now}.json')
	with open(filepath, 'w', encoding='utf-8') as f:
		json.dump(data, f, indent=2, ensure_ascii=False)
	print('saved', filepath)

def pick(items, indices):
	yield from (items[i-1] for i in indices if 0 < i <= len(items))
