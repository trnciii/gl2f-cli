import argparse
from .util import member, article
from .ls import pretty, ls


def add_args(parser):
	ls.add_args(parser)
	pretty.add_args(parser)


def core(args):
	lister = ls.Lister('news', debug=args.dump_response)
	pretty.post_argparse(args)

	fm = pretty.Formatter(f=args.format, fd=args.date_format, sep=args.sep, preview=args.preview)
	fm.reset_index(digits=len(str(args.number)))

	for i in lister.list_group(args.name, args.number, args.page, args.order):
		fm.print(i)
		if args.dl_media:
			article.save_media(i, dump=args.dump_response)


def main():
	parser = argparse.ArgumentParser()
	add_args(parser)
	args = parser.parse_args()

	core(args)
