from . import board, member, date
from ..ayame import terminal as term, zen

class Formatter:
	def __init__(self, f='author:title:url', fd=None, sep=' '):
		self.fstring = f
		self.fdstring = fd if fd else '%m/%d'
		self.sep = sep

		self.index = 0
		self.digits = 2

	def reset_index(self, i=0, digits=2):
		self.index = i
		self.digits = digits


	def author(self, item):
		_, v = member.from_id(item.get('categoryId'))
		if v:
			fullname = v['fullname']
			group = board.get('id', item['boardId'])['group']
			colf, colb = v['color'][group].values()
		else:
			fullname = item.get('category', {'name':''})['name']
			colf, colb = [255, 255, 255], [157, 157, 157]

		return zen.ljust(
			term.mod(fullname, term.bold(), term.rgb(*colf), term.rgb(*colb, 'b')),
			2*member.name_width()
		)

	def title(self, item):
		return term.mod(item['values']['title'], term.bold())

	def url(self, item):
		return term.mod(board.content_url(item), term.dim())

	def date_p(self, item):
		return date.to_datetime(item['openingAt']).strftime(self.fdstring)

	def date_c(self, item):
		return date.to_datetime(item['createdAt']).strftime(self.fdstring)

	def breakline(self, item):
		return '\n'

	def inc_index(self, item):
		self.index += 1
		return f'{self.index:{self.digits}}'

	def content_id(self, item):
		return item['contentId']

	def media_stat(self, item):
		from . import article
		re = article.media_stat(item['values']['body'])
		return self.sep.join([f'i{re["image"]:02}', f'v{re["video"]}'])

	def page(self, item):
		return board.get('id', item['boardId'])['key']


	def format(self, item):
		dic = {
			'author': self.author,
			'title': self.title,
			'url': self.url,
			'date-p': self.date_p,
			'date-c': self.date_c,
			'index': self.inc_index,
			'br': self.breakline,
			'id': self.content_id,
			'media': self.media_stat,
			'page': self.page,
		}

		return self.sep.join(dic[key](item) for key in self.fstring.split(':'))

	def print(self, item, end='\n'):
		print(self.format(item), end=end)


def add_args(parser):
	parser.add_argument('--format', '-f', type=str, default='author:title:url',
		help='format of items. default is "author:title:url"')

	parser.add_argument('--sep', type=str, default=' ',
		help='separator string.')

	parser.add_argument('--break-urls', action='store_true',
		help='break before url')

	parser.add_argument('--date', '-d', type=str, nargs='?', const='%m/%d',
		help='date formatting')

	parser.add_argument('--enum', action='store_true',
		help='show index on the left (lefter than date)')


def make_format(args):
	f = args.format.strip(':')

	if args.break_urls:
		f = f.replace('url', 'br:url')

	if args.date and 'date-p' not in f:
		f = 'date-p:' + f

	if args.enum:
		f = 'index:' + f

	return f


def from_args(args):
	return Formatter(f=make_format(args), fd=args.date, sep=args.sep)
