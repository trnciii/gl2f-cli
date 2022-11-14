from .core import lister, pretty

def name(): return 'search'

def merge(ranges):
	ret = []
	cur = ranges[0]
	for j in range(1, len(ranges)):
		if cur[1] < ranges[j][0]:
			ret.append(cur)
			cur = ranges[j]
		else:
			cur = cur[0], ranges[j][1]
	ret.append(cur)
	return ret


def add_args(parser, list_board):
	lister.add_args(parser)
	pretty.add_args(parser)

	parser.add_argument('keywords', nargs='+')

	def subcommand(args):
		from .core import article, terminal as term
		import re

		fm = pretty.from_args(args)
		fm.reset_index(digits=len(str(args.number)))

		hi = re.compile( fr"(?P<match>{'|'.join(args.keywords)})" )

		items = list_board(args)
		texts = [article.to_text(i, 'plain', False) for i in items]
		counts = [[k in t for k in args.keywords].count(True) for t in texts]

		for c, t, i in sorted(zip(counts, texts, items), reverse=True, key=lambda x:x[0]):
			if c == 0: break

			fm.print(i)

			ranges = [(i.start()-20, i.end()+20) for i in hi.finditer(t)]
			merged = merge(ranges)

			for begin, end in merged:
				print('> ' + hi.sub(
					term.mod(r'\g<match>', term.color('yellow'), term.inv()),
					t[max(0, begin):min(len(t), end)] + term.reset()
				))

			print()


	parser.set_defaults(handler=subcommand)
