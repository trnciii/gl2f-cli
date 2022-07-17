import requests
import os
import sys, argparse
from . import member, util


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


class Formatter:
	def __init__(self, f='author|title|url', fd='%m/%d', sep=' '):
		self.url_parent = None
		self.fstring = f
		self.fdstring = fd
		self.sep = sep

	def set_group(self, group):
		self.url_parent = blog_url(group)

	def format(self, item, end='\n'):
		dic = {
			'author': item['category']['name'],
			'title': item['values']['title'],
			'url': os.path.join(self.url_parent, item['contentId']),
			'date-p': util.to_datetime(item['openingAt']).strftime(self.fdstring),
			'date-c': util.to_datetime(item['createdAt']).strftime(self.fdstring),
			'\\n': '\n',
		}

		return self.sep.join(dic[key] for key in self.fstring.split('|'))


def list_group(group, size=10, page=1, formatter=Formatter()):
	formatter.set_group(group)
	items = fetch(group, size, page)['list']
	print(*[formatter.format(i) for i in items], sep='\n')


def list_member(name, group=None, size=10, page=1, formatter=Formatter()):
	if not group in member.belongs_to(name):
		group = member.belongs_to(name)[0]

	formatter.set_group(group)

	listed = 0
	while listed<size:
		items = list(filter(
			lambda i: i['category']['name'] == member.full_name(name),
			fetch(group, size*3, page)['list']))

		print(*[formatter.format(i) for i in items], sep='\n')

		listed += len(items)
		page += 1

	return page


def parse_args():
	parser = argparse.ArgumentParser()

	# listing
	parser.add_argument('name', type=str,
		help='group or member name')

	parser.add_argument('-s', '--size', type=int, default=10,
		help='number of articles in [1, 99]')

	parser.add_argument('-p', '--page', type=int, default=1,
		help='page number')

	parser.add_argument('--group', type=str,
		help='specify group when name is a member.')


	# formatting
	parser.add_argument('--format', '-F', type=str, default='author|title|url',
		help='formatting. list {author, date-p(published), date-c(created), title, url, \\n} with | separator. default="author|data-p|title|url"')

	parser.add_argument('--date-format', '-Fd', type=str, default='%m/%d',
		help='date formatting.')

	parser.add_argument('--sep', type=str, default=' ',
		help='separator string.')

	parser.add_argument('--break-urls', action='store_true',
		help='break before url')


	args = parser.parse_args()

	if args.break_urls:
		args.format = args.format.replace('url', '\\n|url')

	return args

def ls():
	argv = parse_args()
	pr = Formatter(f=argv.format, fd=argv.date_format, sep=argv.sep)

	if member.is_group(argv.name):
		list_group(argv.name, argv.size, argv.page, formatter=pr)

	elif member.is_member(argv.name):
		list_member(argv.name, group=argv.group, size=argv.size, formatter=pr)
