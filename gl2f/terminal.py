def justzen(s, w):
	if w>len(s):
		return s + '　'*(w-len(s))
	else:
		return s

def rgb(r, g, b, bg='f'):
	if bg in ['b', 'bg', 'background']:
		return f'\033[48;2;{r};{g};{b}m'
	else:
		return f'\033[38;2;{r};{g};{b}m'

def reset_all():
	return '\033[m'

def reset_color():
	return '\033[0m'

def bold():
	return '\033[1m'

def dim():
	return '\033[2m'

def italic():
	return '\033[3m'

def underline():
	return '\033[4m'

def blink():
	return '\033[5m'

def inv():
	return '\033[7m'

def hide():
	return '\033[8m'

def strikeline():
	return '\033[9m'

def mod(s, cc):
	return ''.join(cc) + s + reset_all()
