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


def move_cursor(n):
	if n<0:
		print(f'\033[{-n}A')
	elif n>0:
		print(f'\033[{n}B')

if os.name == 'nt':
	import msvcrt, sys

	def query(q, end):
		sys.stdout.write(q)
		sys.stdout.flush()

		s = ''
		while True:
			c = msvcrt.getch().decode('ascii')
			s += c
			if c == end:
				break
		return s


	def select(items):
		print(mod(" { space: toggle, 'a': all, 'c': clear }", [color('yellow', 'fl')]))
		n = len(items)
		selected = [False]*n
		cursor = 0
		while True:
			cursor = max(0, min(cursor, n-1))

			for i, (item, s) in enumerate(zip(items, selected)):
				clean_row()
				print(('>' if cursor==i else ' ') + ('[x]' if s else '[ ]'), item)

			ch = msvcrt.getch()
			# print(ch)

			if ch == b'\r':
				return selected

			elif ch == b'\x03':
				exit()

			elif ch == b'a':
				selected = [True]*n
			elif ch == b'c':
				selected = [False]*n
			elif ch == b' ':
				selected[cursor] = not selected[cursor]

			elif ch == b'\xe0':
				ch = msvcrt.getch()
				if ch == b'H':
					cursor -= 1
				elif ch == b'P':
					cursor += 1

			move_cursor(-n-1)


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


	def select(items):
		fd = sys.stdout.fileno()

		old = termios.tcgetattr(fd)
		tc = termios.tcgetattr(fd)
		tc[3] &= ~(termios.ICANON | termios.ECHO)

		try:
			termios.tcsetattr(fd, termios.TCSANOW, tc)

			print(mod("space: toggle, 'a': all, 'c': clear", [color('yellow', 'fl')]))
			n = len(items)
			selected = [False]*n
			cursor = 0
			while True:
				cursor = max(0, min(cursor, n-1))

				for i, (item, s) in enumerate(zip(items, selected)):
					clean_row()
					print(('>' if cursor==i else ' ') + ('[x]' if s else '[ ]'), item)

				ch = sys.stdin.read(1)
				# print(ch)

				if ch == '\n':
					return selected

				elif ch == 'a':
					selected = [True]*n
				elif ch == 'c':
					selected = [False]*n
				elif ch == ' ':
					selected[cursor] = not selected[cursor]

				elif ch == '\x1b':
					ch = sys.stdin.read(2)
					if ch == '[A':
						cursor -= 1
					elif ch == '[B':
						cursor += 1

				move_cursor(-n-1)

		finally:
			termios.tcsetattr(fd, termios.TCSANOW, old)

else:
	raise InportError('terminal working on unknown os.')