from .core import config
import os

# editors
def make_string_editor(message):
	return lambda _:input(f'{message}: ')

def make_strings_editor(message, sep=' '):
	return lambda _:input(f'{message}: ').split(sep)

def make_numbers_editor(message, length=1):
	return lambda _:tuple(map(int, input(f'{message}: ').split(maxsplit=length)[:length]))

def make_number_editor(message):
	return lambda _:int(input(f'{message}: ').split(maxsplit=1)[0])

def addons_editor(addons):
	from .ayame import terminal as term

	addons = set(addons)

	todo = term.selected(['add', 'remove'])

	if 'add' in todo:
		addons |= set(make_strings_editor('Addons to add (separated by space)?')(None))
	if 'remove' in todo:
		addons -= set(term.selected(addons))

	valid, error = config.validate_addons(addons)
	if error:
		print('Addons with error (config.addons are kept)')
		for a, e in error:
			print(f'{term.mod(a, term.color("red"))}: {type(e)} {e}')

	return list(addons)

def get_editors():
	return {
		'max-image-size': make_numbers_editor('width height in pixels', 2),
		'serve-port': make_number_editor('port'),
		'host-name': make_string_editor('host name'),
		'addons': addons_editor,
	}

def edit():
	from .ayame import terminal as term

	editors = get_editors()
	data = config.data
	print(data)

	for key in term.selected(list(editors.keys()), lambda k:f'{k}: {data.get(k, f"{str(config.data[k])} (default)")}'):
		try:
			data[key] = editors[key](data[key])
		except Exception as e:
			print(term.mod('error', term.color('red')), e)
			return

	config.save(data)


def view():
	import json
	path = config.filepath()
	if not os.path.isfile(path):
		print('file does not exist.')
		return

	with open(path, encoding='utf-8') as f:
		print(f.read())

def create():
	path = config.filepath()
	if os.path.isfile(path):
		print('file already exits. abort.')
		return

	config.save(config.default())
	print(f'created "{path}".')

def path():
	path = config.filepath()
	print(path if os.path.isfile(path) else 'file does not exist')

def add_to():
	return 'gl2f', 'config'

def add_args(parser):
	sub = parser.add_subparsers()

	sub.add_parser('create').set_defaults(handler=lambda _:create())
	sub.add_parser('path').set_defaults(handler=lambda _:path())
	sub.add_parser('view').set_defaults(handler=lambda _:view())
	sub.add_parser('edit').set_defaults(handler=lambda _:edit())

	return sub