import argparse
from .util import member
from .ls import Lister, make_main


def core(args):
	lister = Lister('radio', debug=args.dump_response)

	if member.is_group(args.name):
		return lister.list_group(args.name, args.number, args.page, args.order)

	elif member.is_member(args.name):
		return lister.list_member(args.name, args.group, args.number, args.page, order=args.order)


main = make_main(core)
