import os

def return_dir(path):
	if not os.path.exists(path):
		os.makedirs(path)
	return path


def home():
	path = os.path.join(os.path.expanduser('~'), 'gl2f')
	return return_dir(path)

def refdir(path):
	return return_dir(os.path.join(home(), path))
