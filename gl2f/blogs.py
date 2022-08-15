import argparse
from .util import member
from .ls import pretty, ls


def add_args(parser):
	ls.add_args(parser)
	pretty.add_args(parser)


def core(args):
	lister = ls.Lister('blog', debug=args.dump_response)
	pretty.post_argparse(args)

	fm = pretty.Formatter(f=args.format, fd=args.date_format, sep=args.sep, preview=args.preview)
	fm.reset_index(digits=len(str(args.number)))

	if member.is_group(args.name):
		for i in lister.list_group(args.name, args.number, args.page, order=args.order):
			fm.print(i)

	elif member.is_member(args.name):
		for i in lister.list_member(args.name, group=args.group, page=args.page, size=args.number, order=args.order):
			fm.print(i)

	elif args.name == 'today':
		for i in lister.list_today():
			fm.print(i)


def main():
	parser = argparse.ArgumentParser()
	add_args(parser)
	args = parser.parse_args()

	core(args)
