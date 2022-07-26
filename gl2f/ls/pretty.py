from .. import terminal as term, util, member, article
import os

class Formatter:
	def __init__(self, f='author|title|url', fd='%m/%d', sep=' ', preview='compact'):
		self.fstring = f
		self.fdstring = fd
		self.sep = sep
		self.preview = preview

		self.index = 0
		self.digits = 2

	def reset_index(self, i=0, digits=2):
		self.index = i
		self.digits = digits


	def author(self, item):
		try:
			_, v = member.from_id(item['categoryId'])
			fullname = v['fullname']
			colf, colb = v['color'][self.group].values()
		except StopIteration:
			fullname = item['category']['name']
			colf, colb = [255, 255, 255], [157, 157, 157]

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
		return term.mod(os.path.join(self.page_url, item['contentId']), [term.dim()])

	def date_p(self, item):
		return util.to_datetime(item['openingAt']).strftime(self.fdstring)

	def date_c(self, item):
		return util.to_datetime(item['createdAt']).strftime(self.fdstring)

	def text(self, item):
		return '\n{}\n'.format(article.to_text(item['values']['body'], self.preview))

	def breakline(self, item):
		return '\n'

	def inc_index(self, item):
		self.index += 1
		return f'{self.index:{self.digits}}'

	def format(self, item, end='\n'):
		dic = {
			'author': self.author,
			'title': self.title,
			'url': self.url,
			'date-p': self.date_p,
			'date-c': self.date_c,
			'text': self.text,
			'index': self.inc_index,
			'\\n': self.breakline,
		}

		return self.sep.join(dic[key](item) for key in self.fstring.split('|'))


def add_args(parser):
	parser.add_argument('--format', '-f', type=str, default='author|title|url',
		help='formatting specified by a list of  {{ {} }} separated by "|". default "author|title|url".'\
		.format(', '.join(Formatter.format.__code__.co_consts[1]))
	)

	parser.add_argument('--date-format', '-df', type=str, default='%m/%d',
		help='date formatting.')

	parser.add_argument('--sep', type=str, default=' ',
		help='separator string.')

	parser.add_argument('--break-urls', action='store_true',
		help='break before url')

	parser.add_argument('--preview', type=str, nargs='?', const='compact', choices=article.to_text_option,
		help='show blog text')

	parser.add_argument('--date', '-d', action='store_true',
		help='show publish date on the left')

	parser.add_argument('--enum', action='store_true',
		help='show index on the left (lefter than date)')


def post_argparse(args):
	if args.break_urls:
		args.format = args.format.replace('url', '\\n|url')

	if args.date:
		args.format = 'date-p|' + args.format

	if args.enum:
		args.format = 'index|' + args.format

	if args.preview:
		args.format += '|text'
