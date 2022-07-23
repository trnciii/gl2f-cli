import argparse
from . import member
from .ls import pretty, ls


def parse_args():
	parser = argparse.ArgumentParser()

	ls.add_args(parser)
	pretty.add_args(parser)

	args = parser.parse_args()

	pretty.post_argparse(args)

	return args


def list():
	lister = ls.Lister('blog')

	argv = parse_args()
	fm = pretty.Formatter(f=argv.format, fd=argv.date_format, sep=argv.sep)
	fm.reset_index(digits=len(str(argv.number)))

	if member.is_group(argv.name):
		lister.list_group(argv.name, argv.number, argv.page, formatter=fm)

	elif member.is_member(argv.name):
		lister.list_member(argv.name, group=argv.group, size=argv.number, formatter=fm)

	elif argv.name == 'today':
		lister.list_today(formatter=fm)
