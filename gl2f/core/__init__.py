def log(message):
	from . import path
	from datetime import datetime
	import os
	commit = os.popen('git log -n1 --pretty=%h').read().rstrip('\n')
	with open(os.path.join(path.home(), 'log'), 'a') as f:
		f.write(f'{datetime.now()} {commit} {message}\n')
