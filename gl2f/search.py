import re
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

def print_highlighted(result, format, pattern, encoding, max_preview_lines=5):
		term.write_with_encoding(pattern.sub(
			term.mod(r'\g<match>', term.color('yellow'), term.inv()),
			format(result.item)
		) + '\n', encoding)

		merged = merge([(i.start()-20, i.end()+20) for i in pattern.finditer(result.text)])
		if len(merged) > max_preview_lines:
			merged = merged[:max_preview_lines]

		for begin, end in merged:
			term.write_with_encoding('> ' + pattern.sub(
				term.mod(r'\g<match>', term.color('yellow')),
				result.text[max(0, begin):min(len(result.text), end)] + term.reset()
			) + '\n', encoding)

		term.write_with_encoding('\n', encoding)

def subcommand(args):
	keywords = list(filter(len, sum((k.split('　') for k in args.keywords), [])))

	items, _ = lister.list_contents(args)
	results = filter(lambda i:i.score > 0, (FilterResult(i, keywords) for i in items))
	if args.sort:
		results = sorted(results, reverse=True, key=lambda x:x.score)

	fm = pretty.from_args(args)
	fm.reset_index(digits=len(str(args.number)))
	for i in results:
		print_highlighted(i, fm.format, re.compile( fr"(?P<match>{'|'.join(keywords)})" ), args.encoding)


def add_to():
	return 'gl2f', 'search'

def add_args(parser):
	parser.description = 'Search in articles'

	lister.add_args(parser)
	pretty.add_args(parser)

	parser.set_defaults(date='%m/%d', number=30)

	parser.add_argument('keywords', nargs='+')
	parser.add_argument('--encoding')
	parser.add_argument('--sort', action='store_true')

	parser.set_defaults(handler=subcommand)

def set_compreply():
	return '__gl2f_complete_list_args'
