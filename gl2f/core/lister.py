import requests
from . import board, member, auth, util
import os, json, re
from datetime import datetime
from ..ayame import terminal


def fetch(boardId, size, page, order='reservedAt:desc', categoryId=None, dump=False, xauth=None):
	response = requests.get(
		f'https://api.fensi.plus/v1/sites/girls2-fc/texts/{boardId}/contents',
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
		print(response)
		print(response.reason)
		return

	data = response.json()

	if dump:
		name = board.get('id', boardId)['page']
		if categoryId:
			name += f'-{member.from_id(categoryId)[0]}'
		util.dump(dump, name, data)

	return data

def fetch_content(url, dump=False, xauth=None):
	page, contentId = re.search(
		r'https://girls2-fc\.jp/page/(?P<page>.+)/(?P<contentId>.+)',
		url
	).groups()
	boardId = board.get('page', page)['id']

	response = requests.get(
		f'https://api.fensi.plus/v1/sites/girls2-fc/texts/{boardId}/contents/{contentId}',
		headers={
			'origin': 'https://girls2-fc.jp',
			'x-from': 'https://girls2-fc.jp',
			'x-authorization': xauth if xauth else auth.update(auth.load()),
		})

	if not response.ok:
		print(response)
		print(response.reason)
		return

	data = response.json()

	if dump:
		util.dump(dump, f'{page}-{contentId}', data)

	return data


def list_multiple_boards(boardId, args):
	# only returns the 'list' value of boards.
	# category id is fixed to None.
	from concurrent.futures import ThreadPoolExecutor
	from functools import partial

	f = partial(fetch, size=10, page=1, xauth=auth.update(auth.load()), dump=args.dump)
	with ThreadPoolExecutor() as executor:
		results = executor.map(f, boardId)

	return sum((r['list'] for r in results), [])


def get_IDs(domain, m, g):
	data = member.get()[m]
	group_list = data['group']
	group = g if g in group_list else group_list[0]
	return board.get('key', f'{domain}/{group}')['id'], data['categoryId'][domain]


def add_args(parser):
	parser.add_argument('board', type=str,
		help='Board to fetch')

	parser.add_argument('-n', '--number', type=int, default=10,
		help='Number of articles to fetch within [1, 99]')

	parser.add_argument('-p', '--page', type=int, default=1,
		help='Page number')

	parser.add_argument('--order', type=str, default='reservedAt:desc',
		help='Set the order with [reservedAt, name] and [asc, desc]')

	parser.add_argument('--group', type=str, choices={'girls2', 'lucky2', 'lovely2'},
		help='Set group when you fetch a member board')

	parser.add_argument('--dump', type=str, nargs='?', const='.',
		help='Dump response, optionally setting the file name')


def in24h(i):
	return (datetime.now() - util.to_datetime(i['openingAt'])).total_seconds() < 24*3600

def list_contents(args):
	if args.board.startswith('blogs/'):
		sub = args.board.split('/')[1]
		if member.is_group(sub):
			boardId = board.get('key', args.board)['id']
			ret = fetch(boardId, args.number, args.page, args.order, dump=args.dump)
			return ret['list'], ret['totalCount']

		elif member.is_member(sub):
			boardId, categoryId = get_IDs('blogs', sub, args.group)
			ret = fetch(boardId, args.number, args.page, args.order, categoryId=categoryId, dump=args.dump)
			return ret['list'], ret['totalCount']

		elif sub == 'today':
			return list(filter(in24h, list_multiple_boards(
				[board.get('key', f'blogs/{g}')['id'] for g in ['girls2', 'lucky2']],
				args
			))), 1

	elif args.board.startswith('radio/'):
		sub = args.board.split('/')[1]
		if member.is_group(sub):
			boardId = board.get('key', args.board)['id']
			ret = fetch(boardId, args.number, args.page, args.order, dump=args.dump)
			return ret['list'], ret['totalCount']

		elif member.is_member(sub):
			boardId, categoryId = get_IDs('radio', sub, args.group)
			ret = fetch(boardId, args.number, args.page, args.order, categoryId=categoryId, dump=args.dump)
			return ret['list'], ret['totalCount']

	elif args.board.startswith('news/'):
		sub = args.board.split('/')[1]
		if sub == 'today':
			boardId = board.get('key', 'news/family')['id']
			return list(filter(in24h, fetch(boardId, size=10, page=1, dump=args.dump)['list'])), 1

		else:
			boardId = board.get('key', args.board)['id']
			ret = fetch(boardId, args.number, args.page, args.order, dump=args.dump)
			return ret['list'], ret['totalCount']

	elif args.board == 'today':
		table = board.definitions()
		ret = list_multiple_boards([i['id'] for i in table['pages'] if i['key'] in table['active']], args)
		return sorted(filter(in24h, ret), key=lambda i:i['openingAt'], reverse=True), 1

	elif b := board.get('key', args.board):
		ret = fetch(b['id'], args.number, args.page, args.order, dump=args.dump)
		return ret['list'], ret['totalCount']

	elif os.path.isfile(args.board):
		with open(args.board, encoding='utf-8') as f:
			return json.load(f)['list'], 1

class Pager:
	def __init__(self, args):
		self.args = args
		self._max_page = -1

	def flip(self, i):
		self.args.page = i
		items, total_count = list_contents(self.args)
		self._max_page = total_count // self.args.number + 1
		return terminal.SelectionList(items)

	def max_page(self):
		return self._max_page

def selected(args, to_string):
	return terminal.selected(Pager(args), args.page, to_string)
