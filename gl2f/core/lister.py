import requests
import json
import argparse
import os
from .. import auth
from . import board, member
from .date import is_today


def fetch(domain, group, size, page, order='reservedAt:desc', categoryId=None, dump=False):
	response = requests.get(
		board.request_url(domain, group),
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
		query = member.from_id(categoryId)[0] if categoryId else group
		now = datetime.datetime.now().strftime('%y%m%d%H%M%S')
		path = os.path.join(dump, f'{domain}-{query}-{now}.json')
		with open(path, 'w') as f:
			json.dump(response.json(), f, indent=2)

	return response.json()


def list_member(domain, args):
	data = member.get()[args.name]
	group_list = data['group']
	group = args.group if args.group in group_list else group_list[0]
	return fetch(domain, group, args.number, args.page, args.order, categoryId=data['categoryId'][domain], dump=args.dump)['list']


def add_args(parser):
	parser.add_argument('name', type=str,
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
	domain = 'blog'

	if member.is_group(args.name):
		return fetch(domain, args.name, args.number, args.page, args.order, dump=args.dump)['list']

	elif member.is_member(args.name):
		return list_member(domain, args)

	elif args.name == 'today':
		return filter(
			lambda i: is_today(i['openingAt']),
			sum((fetch(domain, group, size=10, page=1, dump=args.dump)['list'] for group in ['girls2', 'lucky2']), [])
		)


def news(args):
	domain = 'news'

	if args.name == 'today':
		return filter(
			lambda i: is_today(i['openingAt']),
			fetch(domain, 'family', size=10, page=1, dump=args.dump)['list']
		)

	else:
		return fetch(domain, args.name, args.number, args.page, args.order, dump=args.dump)['list']


def radio(args):
	domain = 'radio'

	if member.is_group(args.name):
		return fetch(domain, args.name, args.number, args.page, args.order, dump=args.dump)['list']

	elif member.is_member(args.name):
		return list_member(domain, args)


def pg(args):
	domain = 'pg'
	return fetch(domain, args.name, args.number, args.page, args.order, dump=args.dump)['list']


def listers():
	return {
		'blogs': blogs,
		'radio': radio,
		'news': news,
		'pg': pg,
	}


def add_args_boardwise(parser, cmd):
	subparsers = parser.add_subparsers()
	for k in listers().keys():
		cmd.add_args(subparsers.add_parser(k), k)