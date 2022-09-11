import requests
import json
import argparse
import os
from .. import auth
from . import board, member
from .date import is_today


def fetch(boardId, size, page, order='reservedAt:desc', categoryId=None, template='texts', dump=False):
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
			'x-authorization': auth.update(auth.load()),
		})

	if not response.ok:
		return

	if dump:
		import datetime
		boarddata = board.get()[boardId]
		kind = boarddata['kind']
		now = datetime.datetime.now().strftime('%y%m%d%H%M%S')
		if categoryId:
			name, _ = member.from_id(categoryId)
		else:
			name = boarddata['group']

		with open(os.path.join(dump,  f'{kind}-{name}-{now}.json'), 'w') as f:
			json.dump(response.json(), f, indent=2)

	return response.json()


def get_IDs(domain, args):
	data = member.get()[args.name]
	group_list = data['group']
	group = args.group if args.group in group_list else group_list[0]

	if domain == 'blog':
		return board.blogs(group), data['categoryId'][domain]
	elif domain == 'radio':
		return board.radio(group), data['categoryId'][domain]


def add_args(parser):
	parser.add_argument('name', type=str, nargs='?',
		help='group or member name')

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


def blogs(args):
	if member.is_group(args.name):
		boardId = board.blogs(args.name)
		return fetch(boardId, args.number, args.page, args.order, dump=args.dump)['list']

	elif member.is_member(args.name):
		boardId, categoryId = get_IDs('blog', args)
		return fetch(boardId, args.number, args.page, args.order, categoryId=categoryId, dump=args.dump)['list']

	elif args.name == 'today':
		return list(filter(
			lambda i: is_today(i['openingAt']),
			sum((fetch(board.blogs(group), size=10, page=1, dump=args.dump)['list'] for group in ['girls2', 'lucky2']), [])
		))


def news(args):
	if args.name == 'today':
		return list(filter(
			lambda i: is_today(i['openingAt']),
			fetch(board.news('family'), size=10, page=1, dump=args.dump)['list']
		))

	else:
		boardId = board.news(args.name)
		return fetch(boardId, args.number, args.page, args.order, dump=args.dump)['list']


def radio(args):
	if member.is_group(args.name):
		boardId = board.radio(args.name)
		return fetch(boardId, args.number, args.page, args.order, dump=args.dump)['list']

	elif member.is_member(args.name):
		boardId, categoryId = get_IDs('radio', args)
		return fetch(boardId, args.number, args.page, args.order, categoryId=categoryId, dump=args.dump)['list']


def make_simple_lister(boardId):
	return lambda args: fetch(boardId, args.number, args.page, args.order, dump=args.dump)['list']


def listers():
	return {
		'blogs': blogs,
		'radio': radio,
		'news': news,
		'gtube': make_simple_lister('270809837141492901'),
		'shangrila': make_simple_lister('689409591506633568'),
	}


def add_args_boardwise(parser, cmd):
	subparsers = parser.add_subparsers()
	for k in listers().keys():
		cmd.add_args(subparsers.add_parser(k), k)