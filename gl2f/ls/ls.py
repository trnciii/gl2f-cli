import requests
import json
import argparse
from .. import member, util, auth
from . import pretty


class Lister:
	def __init__(self, name):
		if name == 'blog':
			from . import domain_blogs
			self.domain = domain_blogs

		elif name == 'radio':
			from . import domain_radio
			self.domain = domain_radio


	def fetch(self, group, size, page, categoryId=None, order='reservedAt:desc'):
		response = requests.get(
			self.domain.request_url(group),
			params={
				'size': str(size),
				'page': str(page),
				'order': str(order),
				'categoryId': categoryId
			},
			cookies={},
			headers={
				'origin': 'https://girls2-fc.jp',
				'x-from': self.domain.contents_url(group),
				'x-authorization': auth.updated(),
			})

		if response.ok:
			return response.json()
		else:
			print('fetch failed')
			# throw


	def list_group(self, group, size=10, page=1, formatter=pretty.Formatter()):
		formatter.page_url = self.domain.contents_url(group)
		formatter.group = group
		items = self.fetch(group, size, page)['list']
		for i in items:
			print(formatter.format(i))


	def list_member(self, name, group=None, size=10, page=1, formatter=pretty.Formatter()):
		member_data = member.get()[name]
		categoryId = member_data['categoryId'][self.domain.name]
		group_list = member_data['group']
		if not group in group_list:
			group = group_list[0]

		formatter.page_url = self.domain.contents_url(group)
		formatter.group = group

		items = self.fetch(group, size, page, categoryId=categoryId)['list']
		for i in items:
			print(formatter.format(i))


	def list_today(self, formatter=pretty.Formatter()):
		for group in ['girls2', 'lucky2']:
			formatter.page_url = self.domain.contents_url(group)
			formatter.group = group
			items = filter(
				lambda i: util.is_today(i['openingAt']),
				self.fetch(group, size=10, page=1)['list'])

			for i in items:
				print(formatter.format(i))


def add_args(parser):
	parser.add_argument('name', type=str,
		help='group or member name')

	parser.add_argument('-n', '--number', type=int, default=10,
		help='number of articles in [1, 99]')

	parser.add_argument('-p', '--page', type=int, default=1,
		help='page number')

	parser.add_argument('--group', type=str,
		help='specify group when name is a member.')
