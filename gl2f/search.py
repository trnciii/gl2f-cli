import re, os
from .core import lister, pretty, article
from .ayame import terminal as term

class FilterResult:
	def __init__(self, item, keywords):
		self.item = item
		self.text = ''.join(article.lines(item, 'plain', False))
		self.score = sum(int(k in self.text) + int(k in item['values']['title']) for k in keywords)

def merge(ranges):
	if len(ranges) == 0: return []

	ret = []
	cur = ranges[0]
	for r in ranges[1:]:
		if cur[1] < r[0]:
			ret.append(cur)
			cur = r
		else:
			cur = cur[0], r[1]
	ret.append(cur)
	return ret

def filter_by_keywords(items, keywords, sort):
	results = filter(lambda i:i.score > 0, (FilterResult(i, keywords) for i in items))
	if sort:
		results = sorted(results, reverse=True, key=lambda x:x.score)
	return results


def to_lines(result, format, pattern, encoding, max_preview_lines=5):
		title = pattern.sub(term.mod(r'\g<match>', term.color('yellow'), term.inv()), format(result.item))

		merged = merge([(i.start()-20, i.end()+20) for i in pattern.finditer(result.text)])
		if len(merged) > max_preview_lines:
			merged = merged[:max_preview_lines]

		heading = ('> ' + pattern.sub(
				term.mod(r'\g<match>', term.color('yellow')),
				result.text[max(0, begin):min(len(result.text), end)] + term.reset()
			) for begin, end in merged)
		return [title] + list(heading) + ['']

def delimiter():
	width, _ = os.get_terminal_size()
	half = (width-5)//4
	return f'{"-"*half}・_・{"-"*half}'

def subcommand(args):
	keywords = list(filter(len, sum((k.split('　') for k in args.keywords), [])))
	pattern = re.compile( fr"(?P<match>{'|'.join(keywords)})" )

	fm = pretty.from_args(args)
	fm.reset_index(digits=len(str(args.number)))


	def gen():
		yield delimiter()
		args.page = 1
		while True:
			items, total_count = lister.list_contents(args)
			if not items:
				yield delimiter()
				return
			for i in filter_by_keywords(items, keywords, False):
				yield from to_lines(i, fm.format, pattern, args.encoding)
			args.page += 1

	term.scroll(gen())


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
