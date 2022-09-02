import argparse
from ..util import member, article
from . import Lister, lister, pretty


def blogs(args):
	lister = Lister('blog', debug=args.dump_response)

	if member.is_group(args.name):
		return lister.list_group(args.name, args.number, args.page, order=args.order)

	elif member.is_member(args.name):
		return lister.list_member(args.name, group=args.group, page=args.page, size=args.number, order=args.order)

	elif args.name == 'today':
		return lister.list_today()


def news(args):
	lister = Lister('news', debug=args.dump_response)
	return lister.list_group(args.name, args.number, args.page, args.order)


def radio(args):
	lister = Lister('radio', debug=args.dump_response)

	if member.is_group(args.name):
		return lister.list_group(args.name, args.number, args.page, args.order)

	elif member.is_member(args.name):
		return lister.list_member(args.name, args.group, args.number, args.page, order=args.order)



def add_args(parser):
	lister.add_args(parser)
	pretty.add_args(parser)
	article.add_args(parser)

def post_argparse(args):
	pretty.post_argparse(args)


def make_subcommand(core):
	def subcommand(args):
		pretty.post_argparse(args)

		fm = pretty.Formatter(f=args.format, fd=args.date_format, sep=args.sep, preview=args.preview)
		fm.reset_index(digits=len(str(args.number)))

		for i in core(args):
			if args.dl_media:
				article.save_media(i, option=args.dl_media, dump=args.dump_response)
			fm.print(i)

	return subcommand


def make_main(core):
	def main():
		parser = argparse.ArgumentParser()
		add_args(parser)
		make_subcommand(core)(parser.parse_args())

	return main


class subcommand:
	blogs = make_subcommand(blogs)
	news = make_subcommand(news)
	radio = make_subcommand(radio)


class main:
	blogs = make_main(blogs)
	news = make_main(news)
	radio = make_main(radio)