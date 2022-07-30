import argparse
from .util import member
from .ls import pretty, ls


def add_args(parser):
	ls.add_args(parser)
	pretty.add_args(parser)


def core(args):
	lister = ls.Lister('radio', debug=args.dump_response)
	pretty.post_argparse(args)

	fm = pretty.Formatter(f=args.format, fd=args.date_format, sep=args.sep)
	fm.reset_index(digits=len(str(args.number)))

	if member.is_group(args.name):
		lister.list_group(args.name, args.number, args.page, args.order, formatter=fm)

	elif member.is_member(args.name):
		lister.list_member(args.name, args.group, args.number, args.page, order=args.order, formatter=fm)


def main():
	parser = argparse.ArgumentParser()
	add_args(parser)
	args = parser.parse_args()

	core(args)
