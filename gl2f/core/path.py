import os

def return_path(path):
	if not os.path.exists(path):
		os.mkdir(path)
		print('created', path)
	return path


def home():
	path = os.path.join(os.path.expanduser('~'), 'gl2f')
	return return_path(path)

def media():
	path = os.path.join(home(), 'media')
	return return_path(path)

def ls(path):
	return os.listdir(return_path(os.path.join(home(), path)))


if __name__ == '__main__':
	print(home())
	print(media())
	print(ls('media'))