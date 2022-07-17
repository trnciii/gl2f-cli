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


def ls_group(group, size=10, page=1):
	for item in fetch(group, size, page)['list']:
		author = member.full_name(member.id_to_name(item['categoryId']))
		title = item['values']['title']
		url = os.path.join(blog_url(group), item['contentId'])
		print(author, title, url)


def ls_member(name, size=10, group=None):
	if not group in member.belongs_to(name):
		group = member.belongs_to(name)[0]

	page = 0
	listed = 0

	while listed<size:
		page += 1
		response = fetch(group, size*3, page)

		for item in response['list']:
			author = item['category']['name']
			if author == member.full_name(name):
				title = item['values']['title']
				url = blog_url(group) + '/' + item['contentId']
				print(author, title, url)
				listed += 1


def ls():
	parser = argparse.ArgumentParser()

	parser.add_argument('name', type=str,
		help='group or member name')
	parser.add_argument('-s', '--size', type=int, default=10,
		help='number of articles in [1, 99]')
	parser.add_argument('-p', '--page', type=int, default=1,
		help='page number')
	parser.add_argument('--group', type=str,
		help='specify group when name is a member')

	args = parser.parse_args()

	if member.is_group(args.name):
		ls_group(args.name, args.size, args.page)

	elif member.is_member(args.name):
		ls_member(args.name, args.size, args.group)
