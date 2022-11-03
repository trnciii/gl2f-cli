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

		for i in list_board(args):
			text = article.to_text(i, 'compressed', False)
			if all(k in text for k in args.keywords):
				fm.print(i)
				text = hi.sub(term.mod(r'\g<match>', [term.color('yellow'), term.inv()]), text)
				print(f'{text}\n')

	parser.set_defaults(handler=subcommand)
