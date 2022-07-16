import requests
import sys, argparse


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
		'lucky2': 'https://girls2-fc.jp/page/lucky2blogs/',
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
		author = item['category']['name']
		title = item['values']['title']
		url = blog_url(group) + '/' + item['contentId']
		print(author, title, url)


def ls(argv = sys.argv):
	parser = argparse.ArgumentParser()

	parser.add_argument('group', type=str, help='group name')
	parser.add_argument('-s', '--size', default=10, help='number of articles')
	parser.add_argument('-p', '--page', default=1, help='page')

	args = parser.parse_args()


	ls_group(args.group, args.size, args.page)



if __name__ == '__main__':
	ls()