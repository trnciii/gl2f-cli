import argparse
from .util import member, article
from .ls import pretty, ls


def add_args(parser):
	ls.add_args(parser)
	pretty.add_args(parser)
	article.add_args(parser)


def core(args):
	lister = ls.Lister('blog', debug=args.dump_response)
	pretty.post_argparse(args)

	fm = pretty.Formatter(f=args.format, fd=args.date_format, sep=args.sep, preview=args.preview)
	fm.reset_index(digits=len(str(args.number)))

	items = []
	if member.is_group(args.name):
		items = lister.list_group(args.name, args.number, args.page, order=args.order)

	elif member.is_member(args.name):
		items = lister.list_member(args.name, group=args.group, page=args.page, size=args.number, order=args.order)

	elif args.name == 'today':
		items =  lister.list_today()


	for i in items:
		fm.print(i)
		if args.dl_media:
			article.save_media(i, option=args.dl_media, dump=args.dump_response)


def main():
	parser = argparse.ArgumentParser()
	add_args(parser)
	args = parser.parse_args()

	core(args)
