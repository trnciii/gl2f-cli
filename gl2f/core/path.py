import os, re

def return_path(path):
	if not os.path.exists(path):
		os.makedirs(path)
	return path


def home():
	path = os.path.join(os.path.expanduser('~'), 'gl2f')
	return return_path(path)

def ref(path):
	return return_path(os.path.join(home(), path))

def ref_untouch(path):
	return os.path.join(home(), path)

if __name__ == '__main__':
	print(home())
