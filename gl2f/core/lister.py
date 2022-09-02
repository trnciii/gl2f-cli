import requests
import json
import argparse
import os
from .. import auth
from . import board, member
from .date import is_today


class Lister:
	def __init__(self, name, debug=False):
		self.name = name
		self.debug = debug


	def fetch(self, group, size, page, order='reservedAt:desc', categoryId=None):
		response = requests.get(
			board.request_url(self.name, group),
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

		if self.debug:
			import datetime
			query = member.from_id(categoryId)[0] if categoryId else group
			now = datetime.datetime.now().strftime('%y%m%d%H%M%S')
			path = os.path.join(self.debug, f'{self.name}-{query}-{now}.json')
			with open(path, 'w') as f:
				json.dump(response.json(), f, indent=2)

		return response.json()


	def list_group(self, group, size=10, page=1, order='reservedAt:desc'):
		return self.fetch(group, size, page, order)['list']


	def list_member(self, name, group=None, size=10, page=1, order='reservedAt:desc'):
		member_data = member.get()[name]
		categoryId = member_data['categoryId'][self.name]
		group_list = member_data['group']
		if not group in group_list:
			group = group_list[0]

		return self.fetch(group, size, page, order, categoryId=categoryId)['list']


	def list_today(self):
		return filter(
			lambda i: is_today(i['openingAt']),
			sum((self.fetch(group, size=10, page=1)['list'] for group in ['girls2', 'lucky2']), [])
		)


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

	parser.add_argument('--dump-response', type=str, nargs='?', const='.',
		help='dump response from server as ./response.json')
