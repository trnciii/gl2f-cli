from .core import lister, pretty, article, terminal as term
import re

def name(): return 'search'

def add_args(parser, list_board):
	lister.add_args(parser)
	pretty.add_args(parser)

	parser.add_argument('keywords', nargs='+')

	def subcommand(args):
		pretty.post_argparse(args)

		fm = pretty.Formatter(f=args.format, fd=args.date, sep=args.sep)
		fm.reset_index(digits=len(str(args.number)))

		hi = re.compile( fr"(?P<match>{'|'.join(args.keywords)})" )

		items = list_board(args)
		texts = [article.to_text(i, 'compressed', False) for i in items]
		counts = [[k in t for k in args.keywords].count(True) for t in texts]

		for c, t, i in sorted(zip(counts, texts, items), reverse=True, key=lambda x:x[0]):
			if c == 0: break
			fm.print(i)
			print(hi.sub(term.mod(r'\g<match>', [term.color('yellow'), term.inv()]), t) + '\n')


	parser.set_defaults(handler=subcommand)
