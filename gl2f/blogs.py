import requests
import os
import json
import argparse
from . import member, util, terminal as term, auth


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


def fetch(group, size, page, order = 'reservedAt:desc', xauth=''):
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
			'x-authorization': xauth,
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
		self.group = group


	def author(self, item):
		k, v = member.from_id(item['categoryId'])
		fullname = v['fullname']
		colf, colb = v['color'][self.group].values()
		mods = [
			term.bold(),
			term.rgb(*colf),
			term.rgb(*colb, 'b')
		]
		return term.justzen(
			term.mod(fullname, mods),
			member.name_width()
		)

	def title(self, item):
		return term.mod(item['values']['title'], [term.bold()])

	def url(self, item):
		return term.mod(os.path.join(self.url_parent, item['contentId']), [term.dim()])

	def date_p(self, item):
		return util.to_datetime(item['openingAt']).strftime(self.fdstring)

	def date_c(self, item):
		return util.to_datetime(item['createdAt']).strftime(self.fdstring)

	def text(self, item):
		return '\n{}\n'.format( '\n'.join(util.paragraphs(item['values']['body'])) )

	def breakline(self, item):
		return '\n'

	def format(self, item, end='\n'):
		dic = {
			'author': self.author,
			'title': self.title,
			'url': self.url,
			'date-p': self.date_p,
			'date-c': self.date_c,
			'text': self.text,
			'\\n': self.breakline,
		}

		return self.sep.join(dic[key](item) for key in self.fstring.split('|'))\
			.replace(f'{self.sep}\n{self.sep}', '\n')


def list_group(group, size=10, page=1, formatter=Formatter()):
	formatter.set_group(group)
	items = fetch(group, size, page, xauth=auth.load())['list']
	print(*[formatter.format(i) for i in items], sep='\n')


def list_member(name, group=None, size=10, page=1, formatter=Formatter()):
	print('more articles may return than specified.')
	member_data = member.from_name(name)

	if not group in member_data['group']:
		group = member_data['group'][0]

	formatter.set_group(group)

	listed = 0
	while listed<size:
		items = list(filter(
			lambda i: member.from_id(i['categoryId'])[0] == name,
			fetch(group, 99, page, xauth=auth.load())['list']))

		print(*[formatter.format(i) for i in items], sep='\n')

		listed += len(items)
		page += 1

	return page


def list_today(formatter=Formatter()):
	for group in ['girls2', 'lucky2']:
		formatter.set_group(group)
		items = filter(
			lambda i: util.is_today(i['openingAt']),
			fetch(group, size=10, page=1, xauth=auth.load())['list'])

		print(*[formatter.format(i) for i in items], sep='\n')


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


	# formatting
	parser.add_argument('--format', '-f', type=str, default='author|title|url',
		help='formatting. list {author, date-p(published), date-c(created), title, url, text, \\n} with "|" separator. default="author|title|url"')

	parser.add_argument('--date-format', '-df', type=str, default='%m/%d',
		help='date formatting.')

	parser.add_argument('--sep', type=str, default=' ',
		help='separator string.')

	parser.add_argument('--break-urls', action='store_true',
		help='break before url')

	parser.add_argument('--preview', action='store_true',
		help='show blog text')

	parser.add_argument('--date', '-d', action='store_true',
		help='show publish date on the left')


	args = parser.parse_args()

	if args.break_urls:
		args.format = args.format.replace('url', '\\n|url')

	if args.date:
		args.format = 'date-p|' + args.format

	if args.preview:
		args.format += '|text'

	return args

def ls():
	argv = parse_args()
	pr = Formatter(f=argv.format, fd=argv.date_format, sep=argv.sep)

	if member.is_group(argv.name):
		list_group(argv.name, argv.number, argv.page, formatter=pr)

	elif member.is_member(argv.name):
		list_member(argv.name, group=argv.group, size=argv.number, formatter=pr)

	elif argv.name == 'today':
		list_today(formatter=pr)
