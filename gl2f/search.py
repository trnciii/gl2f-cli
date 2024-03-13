import re
from .core import lister, pretty, article, util
from .ayame import terminal as term

class FilterResult:
	def __init__(self, item, keywords):
		self.item = item
		self.text = ''.join(article.lines(item, 'plain', False))
		self.score = sum(int(k in self.text) + int(k in item['values']['title']) for k in keywords)

def merge(ranges):
	try:
		cur = next(ranges)
		for r in ranges:
			if cur[1] < r[0]:
				yield cur
				cur = r
			else:
				cur = cur[0], r[1]
		yield cur
	except StopIteration:
		return

def filter_by_keywords(items, keywords, sort):
	results = filter(lambda i:i.score > 0, (FilterResult(i, keywords) for i in items))
	if sort:
		results = sorted(results, reverse=True, key=lambda x:x.score)
	return results


def to_lines(result, format, pattern):
	from itertools import islice, chain

	title = pattern.sub(
		term.mod(r'\g<match>', term.color('yellow'), term.inv()),
		format(result.item)).split('\n')

	make_range = lambda i: (max(0, i.start()-20), min(len(result.text), i.end()+20))
	merged = merge(map(make_range, pattern.finditer(result.text)))

	heading = (pattern.sub(
		term.mod(r'\g<match>', term.color('yellow')),
		f'> {result.text[begin:end]}{term.reset()}'
	) for begin, end in islice(merged, 5))

	return chain(title, heading)

def subcommand(args):
	keywords = list(filter(len, sum((k.split('　') for k in args.keywords), [])))
	pattern = re.compile( fr"(?P<match>{'|'.join(keywords)})" )

	fm = pretty.from_args(args)

	def gen():
		args.page = 1
		while True:
			items, _ = lister.list_contents(args)
			if not items:
				return
			for i in filter_by_keywords(items, keywords, False):
				yield from to_lines(i, fm.format, pattern)
				yield ''
			args.page += 1

	term.scroll(gen(), eof=util.rule)


def add_to():
	return 'gl2f', 'search'

def add_args(parser):
	parser.description = 'Search in articles'

	lister.add_args(parser)
	pretty.add_args(parser)

	parser.set_defaults(date='%y/%m/%d', break_urls=True, number=50)

	parser.add_argument('keywords', nargs='+')
	parser.add_argument('--encoding')
	parser.add_argument('--sort', action='store_true')

	parser.set_defaults(handler=subcommand)

def set_compreply():
	return '__gl2f_complete_list_args'
