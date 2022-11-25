import requests
from .. import auth
from . import board, member
from .date import in24h
import datetime, os, json


def fetch(boardId, size, page, order='reservedAt:desc', categoryId=None, template='texts', dump=False, xauth=None):
	response = requests.get(
		f'https://api.fensi.plus/v1/sites/girls2-fc/{template}/{boardId}/contents',
		params={
			'size': str(size),
			'page': str(page),
			'order': str(order),
			'categoryId': categoryId
		},
		cookies={},
		headers={
			'origin': 'https://girls2-fc.jp',
			'x-from': 'https://girls2-fc.jp',
			'x-authorization': xauth if xauth else auth.update(auth.load()),
		})

	if not response.ok:
		return

	if dump:
		filename = board.get('id', boardId)['page']
		if categoryId:
			name, _ = member.from_id(categoryId)
			filename += f'-{name}'

		now = datetime.datetime.now().strftime('%y%m%d%H%M%S')

		path = os.path.join(dump,  f'{filename}-{now}.json')
		with open(path, 'w', encoding='utf-8') as f:
			json.dump(response.json(), f, indent=2, ensure_ascii=False)
		print('saved', path)

	return response.json()


def list_multiple_boards(boardId, args):
	# only returns the 'list' value of boards.
	# category id and template are fixed.
	from concurrent.futures import ThreadPoolExecutor

	xauth = auth.update(auth.load())
	with ThreadPoolExecutor() as executor:
		futures = [executor.submit(fetch, i, 10, 1, xauth=xauth, dump=args.dump) for i in boardId]

	return sum((f.result()['list'] for f in futures), [])


def get_IDs(domain, m, g):
	data = member.get()[m]
	group_list = data['group']
	group = g if g in group_list else group_list[0]
	return board.get('key', f'{domain}/{group}')['id'], data['categoryId'][domain]


def add_args(parser):
	parser.add_argument('board', type=str,
		help='board and group or member name')

	parser.add_argument('-n', '--number', type=int, default=10,
		help='number of articles in [1, 99]')

	parser.add_argument('-p', '--page', type=int, default=1,
		help='page number')

	parser.add_argument('--order', type=str, default='reservedAt:desc',
		help='order. {reservedAt, name} × {asc, desc}. default = reservedAt:desc.')

	parser.add_argument('--group', type=str,
		help='specify group when name is a member.')

	parser.add_argument('--dump', type=str, nargs='?', const='.',
		help='dump response from server as ./response.json')


def filter_today(li):
	return list(filter(lambda i:in24h(i['openingAt']), li))


def list_contents(args):
	if args.board.startswith('blogs/'):
		sub = args.board.split('/')[1]
		if member.is_group(sub):
			boardId = board.get('key', args.board)['id']
			return fetch(boardId, args.number, args.page, args.order, dump=args.dump)['list']

		elif member.is_member(sub):
			boardId, categoryId = get_IDs('blogs', sub, args.group)
			return fetch(boardId, args.number, args.page, args.order, categoryId=categoryId, dump=args.dump)['list']

		elif sub == 'today':
			return filter_today(list_multiple_boards(
				[board.get('key', f'blogs/{g}')['id'] for g in ['girls2', 'lucky2']],
				args
			))


	elif args.board.startswith('radio/'):
		sub = args.board.split('/')[1]
		if member.is_group(sub):
			boardId = board.get('key', args.board)['id']
			return fetch(boardId, args.number, args.page, args.order, dump=args.dump)['list']

		elif member.is_member(sub):
			boardId, categoryId = get_IDs('radio', sub, args.group)
			return fetch(boardId, args.number, args.page, args.order, categoryId=categoryId, dump=args.dump)['list']


	elif args.board.startswith('news/'):
		sub = args.board.split('/')[1]
		if sub == 'today':
			boardId = board.get('key', 'news/family')['id']
			return filter_today(fetch(boardId, size=10, page=1, dump=args.dump)['list'])

		else:
			boardId = board.get('key', args.board)['id']
			return fetch(boardId, args.number, args.page, args.order, dump=args.dump)['list']


	elif args.board == 'today':
		ret = list_multiple_boards([
			board.get('key', x)['id'] for x in [
				'blogs/girls2',
				'blogs/lucky2',
				'news/family',
				'radio/girls2',
				'radio/lucky2',
				'gtube',
				'cm',
				'shangrila',
				'wallpaper'
			]
		], args)
		return sorted(filter_today(ret), key=lambda i:i['openingAt'], reverse=True)

	else:
		boardId = board.get('key', args.board)['id']
		return fetch(boardId, args.number, args.page, args.order, dump=args.dump)['list']
