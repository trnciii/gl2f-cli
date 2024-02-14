from .core import board

def add_def(args):
	if not args.key:
		d = args.page_id.lower()
		args.key = input(f'set a custom key? (defualt={d})') or d

	if not args.activate:
		args.activate = 'y' == input('set as today\'s page? (y/N)').lower()

	data = board.add(args.page_id, args.key, args.activate)
	if data:
		board.save(data)

def remove_def(key):
	board.save(board.remove(key))

def add_today(key):
	data = board.definitions()
	data['active'].append(key)
	board.save(data)

def remove_today(key):
	data = board.definitions()
	data['active'].remove(key)
	board.save(data)

def show_today():
	print(' '.join(sorted(board.definitions()['active'])))


def add_to():
	return 'gl2f', 'pages'

def add_args(parser):
	parser.description = 'Manage page definitions'

	sub = parser.add_subparsers()

	p = sub.add_parser('add-definition', description='Add a page definition')
	p.add_argument('page_id', type=str)
	p.add_argument('--key', type=str, help='set page name used as command argument')
	p.add_argument('--activate', action='store_true', help='set as today page')
	p.set_defaults(handler=add_def)

	p = sub.add_parser('remove-definition', description='Remove a page definition')
	p.add_argument('key', type=str)
	p.set_defaults(handler=lambda a:remove_def(a.key))

	p = sub.add_parser('add-to-today', description='Add to today pages')
	p.add_argument('page')
	p.set_defaults(handler=lambda a:add_today(a.page))

	p = sub.add_parser('remove-from-today', description='Remove from today pages')
	p.add_argument('page')
	p.set_defaults(handler=lambda a:remove_today(a.page))

	sub.add_parser('show-today', description='Show today pages').set_defaults(handler=lambda _:show_today())

	return sub

def set_compreplies():
	today = ' '.join(board.definitions()['active'])
	return {
		'remove-definition': '__gl2f_complete_list_args',
		'add-to-today': '__gl2f_complete_list_args',
		'remove-from-today': f'COMPREPLY=( $(compgen -W "{today}" -- $cur) )'
	}
