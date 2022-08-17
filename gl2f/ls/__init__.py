from . import pretty, lister
from .lister import Lister
import argparse

def add_args(parser):
	lister.add_args(parser)
	pretty.add_args(parser)


def make_subcommand(core):
	def subcommand(args):
		pretty.post_argparse(args)

		fm = pretty.Formatter(f=args.format, fd=args.date_format, sep=args.sep, preview=args.preview)
		fm.reset_index(digits=len(str(args.number)))

		for i in core(args):
			fm.print(i)

	return subcommand


def make_main(core):
	def main():
		parser = argparse.ArgumentParser()
		add_args(parser)
		make_subcommand(core)(parser.parse_args())

	return main
