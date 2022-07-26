import argparse
from . import member
from .ls import pretty, ls


def add_args(parser):
	ls.add_args(parser)
	pretty.add_args(parser)


def core(args):
	lister = ls.Lister('news', debug=args.dump_response)
	pretty.post_argparse(args)

	fm = pretty.Formatter(f=args.format, fd=args.date_format, sep=args.sep, preview=args.preview)
	fm.reset_index(digits=len(str(args.number)))

	if args.name in {'family', 'girls2', 'lucky2'}:
		lister.list_group(args.name, args.number, args.page, formatter=fm)


def main():
	parser = argparse.ArgumentParser()
	add_args(parser)
	args = parser.parse_args()

	core(args)
