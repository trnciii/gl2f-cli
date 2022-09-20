import os, subprocess
repo = os.path.abspath(os.path.join(os.path.split(__file__)[0], '../../.git'))
git = subprocess.run(f'git --git-dir {repo} log  -n1 --pretty=%h'.split(),
	stdout=subprocess.PIPE, text=True, stderr=subprocess.DEVNULL, shell=(os.name == 'nt'))
commit = git.stdout.rstrip('\n') if git.returncode == 0 else '-'*7

def log(message):
	from . import path
	from datetime import datetime
	with open(os.path.join(path.home(), 'log'), 'a') as f:
		f.write(f'{datetime.now()} {commit} {message}\n')
