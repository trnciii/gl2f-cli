import requests
import os
import sys, argparse
from . import member


def request_url(group):
	url = {
		'girls2': 'https://api.fensi.plus/v1/sites/girls2-fc/texts/271474317252887717/contents',
		'lovely2': 'https://api.fensi.plus/v1/sites/girls2-fc/texts/436708526618837819/contents',
		'lucky2': 'https://api.fensi.plus/v1/sites/girls2-fc/texts/lucky2Blogs/contents'
	}
	return url[group]


def blog_url(group):
	url = {
		'girls2': 'https://girls2-fc.jp/page/blogs',
		'lovely2': 'https://girls2-fc.jp/page/lovely2blogs',
		'lucky2': 'https://girls2-fc.jp/page/lucky2blogs',
	}
	return url[group]


def fetch(group, size, page, order = 'reservedAt:desc'):
	response = requests.get(
		request_url(group),
		params={
	    'size': str(size),
	    'page': str(page),
	    'order': str(order),
		},
		cookies={},
		headers={
	    'origin': 'https://girls2-fc.jp',
	    'x-from': blog_url(group),
		})

	if response.ok:
		return response.json()

	else:
		print('fetch failed')
		# throw


def list_group(group, size=10, page=1):
	for i in fetch(group, size, page)['list']:
		show(i, group)


def list_member(name, group=None, size=10, page=1):
	if not group in member.belongs_to(name):
		group = member.belongs_to(name)[0]

	listed = 0
	while listed<size:
		items = list(filter(
			lambda i: i['category']['name'] == member.full_name(name),
			fetch(group, size*3, page)['list']))

		for i in items:
			show(i, group)
		listed += len(items)
		page += 1

	return page


def show(item, group):
	author = item['category']['name']
	title = item['values']['title']
	url = os.path.join(blog_url(group), item['contentId'])
	published = item['openingAt']
	created = item['createdAt']

	print(author, title, url)


def ls():
	parser = argparse.ArgumentParser()

	# arguments for fetching
	parser.add_argument('name', type=str,
		help='group or member name')

	parser.add_argument('-s', '--size', type=int, default=10,
		help='number of articles in [1, 99]')

	parser.add_argument('-p', '--page', type=int, default=1,
		help='page number')

	parser.add_argument('--group', type=str,
		help='specify group when name is a member')


	argv = parser.parse_args()


	if member.is_group(argv.name):
		list_group(argv.name, argv.size, argv.page)

	elif member.is_member(argv.name):
		list_member(argv.name, group=argv.group, size=argv.size)
