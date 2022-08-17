import argparse
from .util import member
from .ls import Lister, make_main


def core(args):
	lister = Lister('blog', debug=args.dump_response)

	if member.is_group(args.name):
		return lister.list_group(args.name, args.number, args.page, order=args.order)

	elif member.is_member(args.name):
		return lister.list_member(args.name, group=args.group, page=args.page, size=args.number, order=args.order)

	elif args.name == 'today':
		return lister.list_today()


main = make_main(core)