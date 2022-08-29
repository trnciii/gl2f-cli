import re
import os

def justzen(s, w):
	len_displayed = len(re.sub(r'\033\[.*?m', '', s))
	if w>len_displayed:
		return s + '　'*(w-len_displayed)
	else:
		return s

def clean_row():
	w, _ = os.get_terminal_size()
	print('\r' + ' '*(w-1), end='\r', flush=True)


def rgb(r, g, b, bg='f'):
	if bg in ['b', 'bg', 'background']:
		return f'48;2;{r};{g};{b}'
	else:
		return f'38;2;{r};{g};{b}'

def color(name, k='f'):
	table = {
		'black': 0,
		'red': 1,
		'green': 2,
		'yellow': 3,
		'blue': 4,
		'magenta': 5,
		'cyan': 6,
		'white': 7
	}

	kind = {
		'f': 3,
		'b': 4,
		'fl': 9,
		'bl': 10
	}

	assert name in table.keys()
	assert k in kind.keys()

	return str(kind[k]) + str(table[name])


def reset_all():
	return ''

def reset_color():
	return '0'

def bold():
	return '1'

def dim():
	return '2'

def italic():
	return '3'

def underline():
	return '4'

def blink():
	return '5'

def inv():
	return '7'

def hide():
	return '8'

def strikeline():
	return '9'

def mod(s, cc):
	return '\033[{}m'.format(';'.join(cc)) + s + '\033[{}m'.format(reset_all())


if os.name == 'nt':
	import msvcrt, sys

	def query(q, end):
		sys.stdout.write(q)
		sys.stdout.flush()

		s = ''
		while True:
			c = msvcrt.getch().decode('ascii')
			s += c
			if c == 'c':
				break
		return s

elif os.name == 'posix':
	import termios, sys

	def query(q, end):
		fd = sys.stdout.fileno()

		old = termios.tcgetattr(fd)
		tc = termios.tcgetattr(fd)
		tc[3] &= ~(termios.ICANON | termios.ECHO)

		try:
			termios.tcsetattr(fd, termios.TCSANOW, tc)

			sys.stdout.write(q)
			sys.stdout.flush()

			s = ''
			while True:
				c = sys.stdin.read(1)
				s += c
				if c == end:
					break

		finally:
			termios.tcsetattr(fd, termios.TCSANOW, old)

		return s

else:
	raise InportError('terminal working on unknown os.')


if __name__ == '__main__':
	import terminal as term, member

	fullname = '森朱里'
	colf, colb = [255, 255, 255], [32, 203, 115]
	mods = [
		term.bold(),
		term.rgb(*colf),
		term.rgb(*colb, 'b')
	]
	print(term.justzen(
		term.mod(fullname, mods),
		member.name_width()
	))