import requests
import os
import json
import argparse
from . import member, util, auth
from .ls import pretty
from .ls import domain_blogs as domain


def fetch(group, size, page, categoryId=None, order='reservedAt:desc'):
	response = requests.get(
		domain.request_url(group),
		params={
			'size': str(size),
			'page': str(page),
			'order': str(order),
			'categoryId': categoryId
		},
		cookies={},
		headers={
			'origin': 'https://girls2-fc.jp',
			'x-from': domain.contents_url(group),
			'x-authorization': auth.updated(),
		})

	if response.ok:
		return response.json()
	else:
		print('fetch failed')
		# throw


def list_group(group, size=10, page=1, formatter=pretty.Formatter()):
	formatter.page_url = domain.contents_url(group)
	formatter.group = group
	items = fetch(group, size, page)['list']
	for i in items:
		print(formatter.format(i))


def list_member(name, group=None, size=10, page=1, formatter=pretty.Formatter()):
	member_data = member.get()[name]
	categoryId = member_data['categoryId'][domain.name]
	group_list = member_data['group']
	if not group in group_list:
		group = group_list[0]

	formatter.page_url = domain.contents_url(group)
	formatter.group = group

	items = fetch(group, size, page, categoryId=categoryId)['list']
	for i in items:
		print(formatter.format(i))


def list_today(formatter=pretty.Formatter()):
	for group in ['girls2', 'lucky2']:
		formatter.page_url = domain.contents_url(group)
		formatter.group = group
		items = filter(
			lambda i: util.is_today(i['openingAt']),
			fetch(group, size=10, page=1)['list'])

		for i in items:
			print(formatter.format(i))


def parse_args():
	parser = argparse.ArgumentParser()

	# listing
	parser.add_argument('name', type=str,
		help='group or member name')

	parser.add_argument('-n', '--number', type=int, default=10,
		help='number of articles in [1, 99]')

	parser.add_argument('-p', '--page', type=int, default=1,
		help='page number')

	parser.add_argument('--group', type=str,
		help='specify group when name is a member.')


	pretty.add_args(parser)

	args = parser.parse_args()

	pretty.post_argparse(args)

	return args


def ls():
	argv = parse_args()
	fm = pretty.Formatter(f=argv.format, fd=argv.date_format, sep=argv.sep)
	fm.reset_index(digits=len(str(argv.number)))

	if member.is_group(argv.name):
		list_group(argv.name, argv.number, argv.page, formatter=fm)

	elif member.is_member(argv.name):
		list_member(argv.name, group=argv.group, size=argv.number, formatter=fm)

	elif argv.name == 'today':
		list_today(formatter=fm)
